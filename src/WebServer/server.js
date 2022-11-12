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

var result
var infer_result
app.post("/result", async (req, res) => {

  await axios.post('http://localhost:7000/web_handler', {
    name: req.body.name
  })
    .then(function (response) {
      result = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });
  result = JSON.stringify(result)
  json = JSON.parse(result)

  await axios.post('http://localhost:7000/infer_handler', {
    result
  })
    .then(function (response) {
      infer_result = response.data;
    })
    .catch(function (error) {
      console.log(error);
    });

  await res.render('result.html', {
    name: req.body.name,
    decoded_image: infer_result
  })

});