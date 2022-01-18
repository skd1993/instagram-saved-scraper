import json
import codecs
import datetime
import os.path
import argparse
import csv

try:
    from instagram_private_api import (
        Client,
        ClientError,
        ClientLoginError,
        ClientCookieExpiredError,
        ClientLoginRequiredError,
        __version__ as client_version,
    )
except ImportError:
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from instagram_private_api import (
        Client,
        ClientError,
        ClientLoginError,
        ClientCookieExpiredError,
        ClientLoginRequiredError,
        __version__ as client_version,
    )

def create_map_link(coordinates):
  if len(str(coordinates[0]))>0 and len(str(coordinates[1]))>0 :
    return 'https://www.google.com/maps?q=' + str(coordinates[0]) + ',' + str(coordinates[1])
  else:
    return ''

def to_json(python_object):
  if isinstance(python_object, bytes):
      return {
          "__class__": "bytes",
          "__value__": codecs.encode(python_object, "base64").decode(),
      }
  raise TypeError(repr(python_object) + " is not JSON serializable")


def from_json(json_object):
  if "__class__" in json_object and json_object["__class__"] == "bytes":
      return codecs.decode(json_object["__value__"].encode(), "base64")
  return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, "w") as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print("SAVED: {0!s}".format(new_settings_file))


if __name__ == "__main__":

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -c "<collection_id>" -o "output.csv"
    parser = argparse.ArgumentParser(
        description="login callback and save settings"
    )
    parser.add_argument("-u", "--username", dest="username", type=str, required=True)
    parser.add_argument("-p", "--password", dest="password", type=str, required=True)
    parser.add_argument("-c", "--collection", dest="collection", type=str, required=True)
    parser.add_argument("-o", "--output", dest="output", type=str, required=True)

    args = parser.parse_args()

    print("Client version: {0!s}".format(client_version))

    device_id = None
    try:

        settings_file = "credentials.json"
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print("Unable to find file: {0!s}".format(settings_file))

            # login new
            api = Client(
                args.username,
                args.password,
                on_login=lambda x: onlogin_callback(x, settings_file),
            )
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print("Reusing settings: {0!s}".format(settings_file))

            device_id = cached_settings.get("device_id")
            # reuse auth settings
            api = Client(args.username, args.password, settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print("ClientCookieExpiredError/ClientLoginRequiredError: {0!s}".format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username,
            args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, settings_file),
        )

    except ClientLoginError as e:
        print("ClientLoginError {0!s}".format(e))
        exit(9)
    except ClientError as e:
        print(
            "ClientError {0!s} (Code: {1:d}, Response: {2!s})".format(
                e.msg, e.code, e.error_response
            )
        )
        exit(9)
    except Exception as e:
        print("Unexpected Exception: {0!s}".format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    print(
        "Cookie Expiry: {0!s}".format(
            datetime.datetime.fromtimestamp(cookie_expiry).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        )
    )

    print("==== starting to fetch saved posts data")

    saved_collection = []

    results = api.saved_feed()
    saved_collection.extend(results.get("items", []))

    next_max_id = results.get("next_max_id")

    while next_max_id:
        results = api.saved_feed(max_id=next_max_id)
        saved_collection.extend(results.get("items", []))
        next_max_id = results.get("next_max_id")

    field_names = [
        "#",
        "link",
        "location_short_name",
        "facebook_places_id",
        "location_name",
        "address",
        "city",
        "location_lng",
        "location_lat",
        "location_map_link",
        "lng",
        "lat",
        "map_link",
        "full_name_op",
        "username_op",
        "caption",
    ]

    count = 0
    res = []

    print("==== saving data to file")

    for s in saved_collection:
        subset = s.get("media")
        if args.collection in subset["saved_collection_ids"]:
            count = count + 1
            location = subset.get("location", {})
            toAdd = {
                "#": count,
                "link": "https://www.instagram.com/p/" + subset.get("code"),
                "location_short_name": location.get("short_name", ""),
                "facebook_places_id": location.get("facebook_places_id", ""),
                "location_name": location.get("name", ""),
                "address": location.get("address", ""),
                "city": location.get("city", ""),
                "location_lng": location.get("lng", ""),
                "location_lat": location.get("lat", ""),
                "location_map_link": create_map_link([location.get("lat", ""), location.get("lng", "")]),
                "lng": subset.get("lng", ""),
                "lat": subset.get("lat", ""),
                "map_link": create_map_link([subset.get("lat", ""), subset.get("lng", "")]),
                "full_name_op": subset.get("full_name"),
                "username_op": subset.get("username"),
                "caption": subset.get("caption", {}).get("text", ""),
            }
            res.append(toAdd)

    with open(args.output, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(res)
