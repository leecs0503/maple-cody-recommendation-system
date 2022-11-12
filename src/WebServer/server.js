const express = require('express');
const app = express();

const nunjucks = require("nunjucks");

const axios = require('axios');
const { create } = require('domain');



app.set("view engine", "html")
nunjucks.configure("./views", {
    express: app
});


const server = app.listen(3000, () =>{
    console.log("Start Server : localhost: 3000");
}
);



app.use(express.urlencoded({extended: true}));


app.get('/', (req, res) => {
    let name = req.query.data
    res.render('index.html',{
        user: name
    })
  });

var result
app.post("/result", async(req, res)=>{

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
      console.log(result)
      res.render('result.html',{
        data: result
    })

});