const express = require('express')
const app = express();

var client_id = 'dPvUD5AhQ_AnjwC6EAn4';
var client_secret = 'ntmEoi5Gih';

// 기본경로... / 루트 즉. .메인페이지
// 페이지호출
app.get('/', (req,res)=>{
    res.sendFile(__dirname + '/index.html')
})

// 
app.get('/news',(req,res)=>{
    var api_url = 'https://openapi.naver.com/v1/search/news?query=' + encodeURI(req.query.query); // JSON 결과
    var request = require('request');
    var options = {
       url: api_url,
       headers: {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret': client_secret}
    };
    request.get(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
          res.status(200).json(JSON.parse(body));          
        } else {
          res.status(response.statusCode).json({error:'Failed to fetch data'});
        }
      });    
})
app.get('/blog',(req,res)=>{
    var api_url = 'https://openapi.naver.com/v1/search/blog?query=' + encodeURI(req.query.query); // JSON 결과
    var request = require('request');
    var options = {
       url: api_url,
       headers: {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret': client_secret}
    };
    request.get(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
          res.status(200).json(JSON.parse(body));          
        } else {
          res.status(response.statusCode).json({error:'Failed to fetch data'});
        }
      });    
})

// 서버실행
app.listen(3000, ()=>{
    console.log("http://localhost:3000")
})