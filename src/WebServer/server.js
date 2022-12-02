const express = require('express');
const app = express();
const nunjucks = require("nunjucks");
const axios = require('axios');
const { create } = require('domain');


app.use(express.urlencoded({ extended: true }));
app.use(express.json());


app.set("view engine", "html")
nunjucks.configure("./views", {
  express: app
});


app.listen(3000, () => {
  console.log("Start Server : localhost: 3000");
}
);


module.exports = app;

app.get('/', (req, res) => {
  res.render('index.html')
});

var character_code_result
var infer_result
app.post("/result", async (req, res) => {
  await axios.post('http://localhost:7000/character_code_web_handler', {
    name: req.body.name
  })
    .then(function (response) {
      character_code_result = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });


  await axios.post('http://localhost:7000/infer_code_web_handler', {
    character_code_result
  })
    .then(function (response) {
      infer_result = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });

  await res.render('result.html', {
    name: req.body.name,
    infer_image: infer_result['encoding_image_string'],
    code_name: infer_result['infer_item_code_name']
  })
});