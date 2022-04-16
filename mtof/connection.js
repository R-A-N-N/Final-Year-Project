const { MongoClient, ServerApiVersion } = require('mongodb');

const uri = "mongodb+srv://nikita:nik123456@tweets.drdld.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";

const client = new MongoClient(uri, { 
	useNewUrlParser: true, 
	useUnifiedTopology: true, 
	serverApi: ServerApiVersion.v1 
});

client.connect(err => {
  const collection = client.db("Data").collection("Tweet");
  console.log(collection);
  client.close();
});
