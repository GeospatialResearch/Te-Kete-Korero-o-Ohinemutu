'use strict'

const webpack = require('webpack')
const merge = require('webpack-merge')
const baseConfig = require('./webpack.config.base')

const utils = require('./utils')

const HOST = '0.0.0.0'
const PORT = 8080

module.exports = merge(baseConfig, {
  mode: 'development',

  devServer: {
    public: '0.0.0.0:80',
    clientLogLevel: 'warning',
    hot: true,
    contentBase: 'dist',
    compress: true,
    host: HOST,
    port: PORT,
    open: true,
    overlay: { warnings: false, errors: true },
    publicPath: '/',
    quiet: true
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      }, {
        test: /\.styl(us)?$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'stylus-loader'
        ]
      }
    ]
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new webpack.DefinePlugin({
      'process.env.API_HOST': JSON.stringify(utils.parameters.API_HOST),
      'process.env.WEB_HOST': JSON.stringify(utils.parameters.WEB_HOST),
      'process.env.GEOSERVER_HOST': JSON.stringify(utils.parameters.GEOSERVER_HOST),
      'process.env.LINZ_ACCESS_KEY': JSON.stringify(utils.parameters.LINZ_ACCESS_KEY),
      'process.env.MFE_ACCESS_KEY': JSON.stringify(utils.parameters.MFE_ACCESS_KEY)
    })
  ]
})
