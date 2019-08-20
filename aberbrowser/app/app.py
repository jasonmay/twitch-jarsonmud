from flask import Flask, request, jsonify, abort
import json

app = Flask("aberbrowser")

with open("zones.json", "r") as z:
    zones = json.load(z)


@app.route("/")
def all():
    return jsonify(zones)


@app.route("/<entity>/properties")
def properties(entity):
    if entity not in zones:
        abort(404)

    return jsonify(
        list(set([p["name"] for e in zones[entity] for p in e["properties"]]))
    )


@app.route("/search/<entity>/property/<prop>")
def search_properties(entity, prop):
    if entity not in zones:
        abort(404)

    id_only = bool(request.args.get("id_only"))
    q = request.args.get("q", "")
    mode = request.args.get("mode", "exact")

    results = []

    for entity_instance in zones[entity]:
        for p in entity_instance["properties"]:
            if p["name"] == prop:
                if len(q):
                    if mode == "match" and q not in p["value"]:
                        continue
                    if mode == "exact" and q != p["value"]:
                        continue
                if id_only:
                    results.append(entity_instance["id"])
                else:
                    results.append(entity_instance)

    return jsonify(results)


# @app.route("/search/<entity>/property")
# def property_substr(entity, prop):
#    if entity not in zones:
#        abort(404)
#
#    q = request.args.get("q", "")
#
#    id_only = bool(request.args.get("id_only"))
#
#    results = []
#
#    for entity_instance in zones[entity]:
#        for p in entity_instance["properties"]:
#            if p["name"] == prop:
#                if id_only:
#                    results.append(entity_instance["id"])
#                else:
#                    results.append(entity_instance)
#
#    return jsonify(results)
