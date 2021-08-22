const path = require('path');

module.exports = {
  mode: 'development',
  entry: {
    main: './src/main.js',
    cart: './src/cart.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.(scss|css)$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      }
    ]
  }
};