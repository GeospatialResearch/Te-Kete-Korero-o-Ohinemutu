'use strict'

const merge = require('webpack-merge')
const baseConfig = require('./webpack.config.base')
const MiniCssExtractPlugin  = require('mini-css-extract-plugin')
const webpack = require('webpack')
const utils = require('./utils')
const TerserPlugin = require('terser-webpack-plugin')

module.exports = merge(baseConfig, {
  mode: 'production',
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendor",
          chunks: "all",
        },
      },
    },
    minimizer: [
      new TerserPlugin({
        sourceMap: false,
        terserOptions: {
          compress: {
            warnings: false,
            comparisons: false
          },
          output: {
            comments: false
          }
        }
      }),
    ]
  },
  module: {
    rules: [
      {
        test: /\.css?$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }, {
        test: /\.styl(us)?$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'stylus-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'main.css'
    }),
    new webpack.DefinePlugin({
    'process.env.NODE_ENV': '"production"',
    'process.env.API_HOST': JSON.stringify(utils.parameters.API_HOST),
    'process.env.WEB_HOST': JSON.stringify(utils.parameters.WEB_HOST),
    'process.env.GEOSERVER_HOST': JSON.stringify(utils.parameters.GEOSERVER_HOST),
    'process.env.LINZ_ACCESS_KEY': JSON.stringify(utils.parameters.LINZ_ACCESS_KEY),
    'process.env.MFE_ACCESS_KEY': JSON.stringify(utils.parameters.MFE_ACCESS_KEY)
  })
]
})
