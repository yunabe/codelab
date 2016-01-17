var webpack = require('webpack');
var path = require('path');
var ExternalsPlugin = webpack.ExternalsPlugin;

module.exports = {
  // Multiple entry points.
  entry: {
    main: "./main.js",
    view: "./view.js",
  },
  output: {
    path: path.join(__dirname, "dist"),
    filename: "[name].entry.js"
  },
  // Use babel to covert JavaScript.
  module: {
    loaders: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader",
        query: {presets: ['es2015', 'react']}
      }
    ]
  },
  plugins: [
    new ExternalsPlugin('commonjs', ['electron'])
  ],
  // https://webpack.github.io/docs/configuration.html#target
  // It's not working?
  target: 'electron',
  // https://webpack.github.io/docs/configuration.html#node
  // Do not use __dirname mock.
  node: {
    __dirname: false,
  }
};
