	function findSMS(keyWord, dataArray){
            var smsArray=[];
            var reg =  (" " + keyWord + " ")
            for(var i=0; i< dataArray.length; i++){
                for(key in dataArray[i]){
                     if(key=="SMS" && dataArray[i][key].toLowerCase().search(keyWord)!=-1) {
                        smsArray.push(dataArray[i]);
                    }
                }
        }
        return smsArray;
      }
