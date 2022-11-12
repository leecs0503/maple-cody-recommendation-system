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
var infer_code_bs64encoding_result
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
      infer_code_bs64encoding_result = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });


  await res.render('result.html', {
    name: req.body.name,
    decoded_image: infer_code_bs64encoding_result
  })

});