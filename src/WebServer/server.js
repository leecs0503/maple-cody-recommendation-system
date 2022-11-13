const express = require('express');
const app = express();

const nunjucks = require("nunjucks");

const axios = require('axios');
const { create } = require('domain');




app.set("view engine", "html")
nunjucks.configure("./views", {
  express: app
});


const server = app.listen(3000, () => {
  console.log("Start Server : localhost: 3000");
}
);



app.use(express.urlencoded({ extended: true }));


app.get('/', (req, res) => {
  let name = req.query.data
  res.render('index.html', {
    user: name
  })
});

var character_code_result
var infer_result
app.post("/result", async (req, res) => {

  await axios.get('http://localhost:7000/get_wz_code')
    .then(function (response) {
      wz_code = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });


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

  infer_code = infer_result['inference_code']

  var code_name = {}
  for (key in infer_code) {
    value = infer_code[key]
    if (value == 0) {
      continue
    }
    if (key == 'hair') {
      value = value.split('+')[0]
      code_name[key] = wz_code[key][value]['name']
      continue
    }
    if (key == 'skin') {
      key = 'head'
      code_name[key] = wz_code[key][infer_code['skin']]['name']
      continue

    }
    if (key == 'shield') {
      continue
    }
    code_name[key] = wz_code[key][infer_code[key]]['name']
  }

  await res.render('result.html', {
    name: req.body.name,
    infer_image: infer_result['encoding_image_string'],
    code_name: code_name
  })
});