const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use(
        '/v1/recommend-cody',
        createProxyMiddleware({
            target: 'http://vqateam12.kro.kr:8383',
            changeOrigin: true,
        })
    );
    app.use(
        '/v1/character-info',
        createProxyMiddleware({
            target: 'http://vqateam12.kro.kr:8383',
            changeOrigin: true,
        })
    );
    app.use(
        '/v1/infer_code_web_handler',
        createProxyMiddleware({
            target: 'http://vqateam12.kro.kr:8383',
            changeOrigin: true,
        })
    );

};