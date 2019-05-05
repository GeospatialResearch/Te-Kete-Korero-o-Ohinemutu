'use strict'

const path = require('path')

// Start with some defaults for dev.
const parameters = {
  // DATA_HOST: "https://data.esp.gritool.com",
  API_HOST: "http://localhost:8000",
  WEB_HOST: "http://localhost",
  // MAPBOX_ACCESS_TOKEN: "pk.eyJ1IjoiZmFsY29hIiwiYSI6ImNqZTk0YjRubjAyNjUyd3M1NHB3ZnFpNmwifQ.J1BcodUi_iSRyCu-DmPjcQ"
}
// if (process.env.DATA_HOST) {
//   parameters.DATA_HOST = process.env.DATA_HOST
// }
if (process.env.API_HOST) {
  parameters.API_HOST = process.env.API_HOST
}
if (process.env.WEB_HOST) {
  parameters.WEB_HOST = process.env.WEB_HOST
}

console.log("Using parameters: ", parameters)

module.exports = {
  resolve: function (dir) {
    return path.join(__dirname, '..', dir)
  },

  assetsPath: function (_path) {
    const assetsSubDirectory = 'static'
    return path.posix.join(assetsSubDirectory, _path)
  },

  parameters: parameters
}
