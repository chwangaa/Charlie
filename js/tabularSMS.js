		function findSMS(keyWord, dataArray){
            var smsArray=[];
            var reg =  (" " + keyWord + " ")
            for(var i=0; i< dataArray.length; i++){
                for(key in dataArray[i]){
                     if(key=="SMS" && dataArray[i][key].toLowerCase().search(keyWord)!=-1) {
                        //console.log(JSON.stringify(dataArray[i]));
                        smsArray.push(JSON.stringify(dataArray[i])+"<br>");
                    }
                }
        }
        return smsArray;
      }
