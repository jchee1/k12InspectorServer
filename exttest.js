const check = () =>  {
  const res = fetch('http://127.0.0.1:5000/save', {
    headers : {
        'Content-Type' : 'application/json'
    },
    method : 'POST',
    body : JSON.stringify( {
        'UrlLeak' : "hi",
        'PostLeak' : "hi3"
    })
  })
  .then(function (response){
  
      if(response.ok) {
          response.json()
          .then(function(response) {
              console.log(response);
          });
      }
      else {
          throw Error('Something went wrong');
      }
  })
  .catch(function(error) {
      console.log(error);
  });
};

console.log(check())
