'use strict'

const path = require('path')

// Start with some defaults for dev.
const parameters = {
  API_HOST: "http://localhost:8000",
  WEB_HOST: "http://localhost",
  GEOSERVER_HOST: "http://localhost:8080/geoserver",
  LINZ_ACCESS_KEY: "686e9f2c49414b88a87fae01d046dc82",
  MFE_ACCESS_KEY: "16369a2103f04311864cf0fd1cddec3b"
}

if (process.env.API_HOST) {
  parameters.API_HOST = process.env.API_HOST
}
if (process.env.WEB_HOST) {
  parameters.WEB_HOST = process.env.WEB_HOST
  parameters.GEOSERVER_HOST = parameters.WEB_HOST.replace('www', 'geoserver') + '/geoserver'
}

if (process.env.ENVIRONMENT === 'localprod') {
  // This is for testing the production build
  parameters.API_HOST = "http://api.maptool.vcap.me"
  parameters.WEB_HOST = "http://www.maptool.vcap.me"
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
