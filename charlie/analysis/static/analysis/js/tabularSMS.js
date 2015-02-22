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
    $('#pretty').dataTable( {
            data: data,
            columns: [
                { data: 'Index'},
                { data: 'Country'},
                { data: 'RStation'},
                { data: 'SMS'},
                { data: 'opinion',
                  className: "editOpinion"
                }
            ],
            fields: [{
                label: "Index"
            },
            {
                label: "opinion:",
                name:  "opinion",
                type:  "radio",
                options: [
                    { label: "To do", value: 0 },
                    { label: "Done",  value: 1 }
                ],
                "default": 0
            },],
            "scrollY": "500px",
            "scrollCollapse": true,
            "paging": false,
            "jQueryUI": true
        } );
}

function displayTable(opinion){
    d = filterBy(data_filtered, 'opinion', opinion)
    updateList(d)
    CTR_WINDOW = WINDOW.LIST
    switchView()
}

function displayTable(opinion, country){
    d1 = filterBy(data_filtered, 'opinion', opinion)
    d2 = filterBy(d1, 'Country', country)
    updateList(d2)
    CTR_WINDOW = WINDOW.LIST
    switchView()
}