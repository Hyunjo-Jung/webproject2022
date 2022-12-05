//서버 만들기 express

const express = require('express');
const http = require('http');
const app = express();
const port = 8000;


//express 서버 테스트
//미들웨어 만들기
app.use((req, res, next) => {
    console.log('미들웨어 실행');
    next();
});

//고정폴더로 public 사용
app.use(express.static('public'));
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
}
);

//stockindex.html 라우팅
app.get('/stockindex', (req, res) => {
    res.sendFile(__dirname + '/public/stockindex.html');
}
);
//ETF.html 라우팅
app.get('/ETF', (req, res) => {
    res.sendFile(__dirname + '/public/ETF.html');
}
);
//bond.html 라우팅
app.get('/bond', (req, res) => {
    res.sendFile(__dirname + '/public/bond.html');
}
);
//corr.html 라우팅
app.get('/corr', (req, res) => {
    res.sendFile(__dirname + '/public/corr.html');
}
);


app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});






