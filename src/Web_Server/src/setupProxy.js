const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        '/character_code_web_handler',
        createProxyMiddleware({
            target: 'http://localhost:7000',
            changeOrigin: true,
        })
    );
    app.use(
        '/infer_code_web_handler',
        createProxyMiddleware({
            target: 'http://localhost:7000',
            changeOrigin: true,
        })
    );

};