var Product = require('../models/product');
var mongoose = require('mongoose');
var uri = 'mongodb+srv://test190520:test190520@cluster0-gzdzv.azure.mongodb.net/test?retryWrites=true';

// Connect to mongo
mongoose.connect(uri, {
    useNewUrlParser: true
});
//mongoose.connect(uri, { dbName: 'ShoppingCart' });
var products = [
    new Product({
        imagePath: 'https://images.homedepot-static.com/productImages/6f82b010-9be7-41ce-8eae-6fa528c1b84b/svn/purple-zest-candle-candles-cbz-034-64_1000.jpg',
        title: 'Purple_Ball',
        description: '葡萄美酒夜光杯，奼紫嫣紅手上有',
        price: 545
    }),
    new Product({
        imagePath: 'https://g-search1.alicdn.com/img/bao/uploaded/i5/TB2Bt9nqeuSBuNjSsziXXbq8pXa_!!672292944.jpg_300x300.jpg',
        title: 'Blue_Ball',
        description: '小軒窗，正梳妝，堅決要投藍黨球，哭~',
        price: 444
    }),
    new Product({
        imagePath: 'https://img.pcstore.com.tw/~prod/M12381698_big.jpg?pimg=static&P=1519377067',
        title: 'Orange_Ball',
        description: '橘球雖要九千九，召喚神龍你要有',
        price: 9999
    }),
    new Product({
        imagePath: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrX7qE_HgmP2GdVTgx5QY24jyEsLfurem_XdFEstMEA-oGo4Hx',
        title: 'Green_Ball',
        description: '老闆自掛東南枝，一頂綠球九九九',
        price: 999
    }),
    new Product({
        imagePath: 'https://mydesycdn.mydesy.com/wp-content/uploads/2016/12/Red-Ball-Project12.jpg',
        title: 'Red_Ball',
        description: '商女不知亡國恨，盜賣紅球兩千有',
        price: 2000
    }),
    new Product({
        imagePath: 'https://stickershop.line-scdn.net/stickershop/v1/product/1151965/LINEStorePC/main.png;compress=true',
        title: 'Yellow_Ball',
        description: '此球應為天上有，入手只要一千九',
        price: 1900
    }),
    //https://leafyeh.com/post-117703801/
    new Product({
        imagePath: 'https://leafyeh.com/wp-content/uploads/flickr/37544591291_5a2a830652_o.jpg',
        title: '【台北公館】池先生-肉骨茶',
        description: '正宗大馬味，咖哩叻沙、肉骨茶通通吃得到！',
        price: 190
    }),
    //https://www.gomaji.com/store/76848?pid=227141&gid=31171
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/848/76848/218791/76848-218791-m-1551055194.jpg',
        title: '台北喜來登大飯店-十二廚',
        description: '假日下午茶自助吃到飽餐券',
        price: 899
    }),
    //https://www.gomaji.com/store/116872?pid=227380&gid=155375
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/872/116872/226877/116872-226877-m-1557371010.jpg',
        title: '台北神旺大飯店-普諾麵包坊',
        description: '6吋蛋糕提貨券',
        price: 545
    }),
    //https://www.gomaji.com/store/69441?pid=227318&gid=27560
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/441/69441/218627/69441-218627-m-1543549783.jpg',
        title: 'The Kitchen Table西餐廳',
        description: '平日午餐自助吃到飽雙人券(可適用於週一自助晚餐)',
        price: 1810
    }),
    //https: //www.gomaji.com/store/18105?pid=224624&gid=12635
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/105/18105/224624/18105-224624-m-1553746070.jpg',
        title: '台北晶華酒店-栢麗廳',
        description: '平日晚餐單人吃到飽',
        price: 1399
    }),
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/796/135796/227435/IMG_2272.jpg',
        title: 'MJs Pizza Bar瑪莉珍(信義店)',
        description: '瑪莉珍道地義式美味雙人餐',
        price: 379
    }),
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/683/16683/226104/16683-226104-m-1556590252.jpg',
        title: '天香回味(復北店)',
        description: '搶鍋夏酒菜雙人饗宴',
        price: 999
    }),
    new Product({
        imagePath: 'https://picdn.gomaji.com/products/o/91/227091/227091_1.jpg',
        title: 'SMOR GAFE',
        description: '平假日皆可抵用350元消費金額',
        price: 258
    }),
    new Product({
        imagePath: 'https://picdn.gomaji.com/uploads/stores/866/22866/227065/22866-227065-m-1558324864.jpg',
        title: '墨賞新鐵板料理',
        description: '平日限定-季節鮮魚海陸套餐',
        price: 968
    }),
    new Product({
        imagePath: 'https://picdn.gomaji.com/products/o/342/227342/227342_1.jpg',
        title: '樂饗精緻鍋物(中和店)',
        description: '平假日皆可抵用400元消費金額',
        price: 235
    })
];

var done = 0;
for (var i = 0; i < products.length; i++) {
    products[i].save(function(err, result) {
        done++;
        if (done === products.length) {
            exit();
        }
    });

}

function exit() {
    mongoose.disconnect();
}