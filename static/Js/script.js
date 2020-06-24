$(document).ready(function(){
  $('#select-name').selectize({plugins: ['remove_button']
}
);
});

$(document).ready( function () {
    $('#mydatatable').DataTable();
} );


var table=document.getElementById("mydatatable");
var rows=table.rows;
var headerz = document.createElement("TH");
headerz.innerHTML += "Suitability";
rows[0].append(headerz);

for(var i = 1; i < rows.length ; i++){

 var cells = rows[i].cells;
 var sum = 0;

for(var x = 1; x < cells.length - 1 ; x++){
    var cell = cells[x];
    //console.log(cell.innerHTML + "vallllllllls")
    sum += parseInt(cell.innerHTML);

}
//console.log(sum + "summmmmmm")
//console.log(cells.length + "length")
var average = sum/(cells.length -2);
//console.log(average + "avggggggg")
//lastCell = $("tr:not(:first)");
lastCell = $('td:last-child');
//console.log(average)
lastCell[i-1].append(average);

}



for(var num = 0; num < $('td:last-child').length; num++){

    if ($('td:last-child:eq('+ num +')').text() < 4){
        $('td:last-child:eq('+ num +')').text("Low").css('background','red');

    }else if ($('td:last-child:eq('+ num +')').text() < 8 && $('td:last-child:eq('+ num +')').text() >=4){
        $('td:last-child:eq('+ num +')').text("Medium").css('background','orange');
    }else{
        $('td:last-child:eq('+ num +')').text("High").css('background','green');
    }

}


//Hover for cv link

//var lis = document.getElementsByClassName("nav-link");
//lis.addEventListener("mouseover", function() {
//    this.getElementsByTagName("a").style.color = "white";
//  });
//  lis.addEventListener("mouseout", function() {
//    this.getElementsByTagName("a")[0].style.color = "red";
//  });
