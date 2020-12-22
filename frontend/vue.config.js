module.exports = {
    lintOnSave: 'error',
    publicPath: process.env.NODE_ENV === 'production' ? './static/dist' : '/',
    filenameHashing: false,
    devServer: {
        proxy: 'http://localhost:8000',
        disableHostCheck: true,
        port: 8080
    }
}
