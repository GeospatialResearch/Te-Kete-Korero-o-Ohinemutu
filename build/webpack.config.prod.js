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
    // 'process.env.DATA_HOST': JSON.stringify(config.parameters.DATA_HOST),
    'process.env.API_HOST': JSON.stringify(utils.parameters.API_HOST),
    'process.env.WEB_HOST': JSON.stringify(utils.parameters.WEB_HOST),
    // 'process.env.MAPBOX_ACCESS_TOKEN': JSON.stringify(config.parameters.MAPBOX_ACCESS_TOKEN)
  })
]
})
