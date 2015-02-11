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

function updateList(data){
    if(CTR_TABLE_INITIALIZED == true){
        $('#pretty').dataTable().fnDestroy();
    }
    else{
        CTR_TABLE_INITIALIZED = true
    }
    $('#pretty').DataTable( {
            data: data,
            columns: [
                { data: 'Country'},
                { data: 'RStation'},
                { data: 'SMS'},
                { data: 'opinion'}
            ]
        } );
}
