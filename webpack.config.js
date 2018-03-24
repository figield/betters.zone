var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var CleanWebpackPlugin = require('clean-webpack-plugin');

var extractPlugin = new ExtractTextPlugin({
	filename: 'main.css'
});

module.exports = {
	entry: './static_src/js/app.js',
	output: {
		path: path.resolve(__dirname, 'static/dist'),
		filename: 'bundle.js'
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				use: [
					{
						loader: 'babel-loader',
						options: {
							presets: ['es2015']
						}
					}
				]
			},
		    {
		      test: /\.scss$/,
		      use: extractPlugin.extract({
		      	use: ['css-loader', 'sass-loader']
		      })
		    },
		    // the url-loader uses DataUrls. 
			{ 
			  test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
			  loader: 'url-loader?limit=10000&mimetype=application/font-woff'
			},
			// the file-loader emits files. 
			{ 
			  test: /\.(otf|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, 
			  loader: 'file-loader'
			},
			{
		      test: /\.html$/,
		      use: ['html-loader']
		    },
		    {
		      test: /\.(png|jpg|gif)$/,
		      use: [
		        {
		          loader: 'url-loader',
		          options: {
		            limit: 8192
		          }
		        }
		      ]
		    }
		],
	},
	plugins: [
		extractPlugin,
		new webpack.optimize.UglifyJsPlugin({}),
		new HtmlWebpackPlugin({
			template: 'templates/base.html'
		}),
		new CleanWebpackPlugin(['dist'])
	]
};