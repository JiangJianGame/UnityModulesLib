/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1432389269")

  // update collection data
  unmarshal({
    "name": "types"
  }, collection)

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1432389269")

  // update collection data
  unmarshal({
    "name": "resource_types"
  }, collection)

  return app.save(collection)
})
