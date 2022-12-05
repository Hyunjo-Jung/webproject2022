dfd.read_csv("public/D200index.csv")


//나스닥 다우 에센피 각각 따로 그래프
dfd.read_csv("public/D200index.csv")
.then(df => {
    var layout = {
        //title: 'D200 Index',
        //x축 이름
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
new_df.plot("plot_div1").line({ columns: ["Nasdaq"], layout: layout 
})
}).catch(err => {
    console.log(err);
})

dfd.read_csv("public/D200index.csv")
.then(df => {
    var layout = {
        //title: 'D200 Index',
        //x축 이름
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
new_df.plot("plot_div2").line({ columns: ["DJIA"], layout: layout
})
}).catch(err => {
    console.log(err);
}
) 

dfd.read_csv("public/D200index.csv")
.then(df => {
    var layout = {
        //title: 'D200 Index',
        //x축 이름
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
new_df.plot("plot_div3").line({ columns: ["S&P500"], layout: layout
})
}).catch(err => {
    console.log(err);
}
)

dfd.read_csv("public/ETF_scale.csv")
.then(df => {
    var layout = {
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
//QQQ,SOXX,XBI,XOP,IYH 칼럼
new_df.plot("plot_div4").line({ columns: ["QQQ","SOXX","XBI","XOP","IYH"], layout: layout
})
}).catch(err => {
    console.log(err);
}
)

dfd.read_csv("public/bond_rate.csv")
.then(df => {
    var layout = {
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
//기준금리,SHY,IEF,TLT 칼럼
new_df.plot("plot_div5").line({ columns: ["기준금리"], layout: layout
})
}).catch(err => {
    console.log(err);
}
)

//,"SHY","IEF","TLT"
dfd.read_csv("public/bond_rate.csv")
.then(df => {
    var layout = {
        xaxis: {title: 'Date'},
        yaxis: {title: 'Count'}
    }
new_df = df.set_index({ key: "Date" })
new_df.plot("plot_div6").line({ columns: ["SHY","IEF","TLT"], layout: layout
})
}
).catch(err => {
    console.log(err);
}
)
