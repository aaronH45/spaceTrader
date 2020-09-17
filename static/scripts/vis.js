function travel(id, fuelCost) {
    var area = document.getElementById("planetArea");
    var elems = document.getElementsByClassName('planet');
    var inven = document.getElementById("inventory");
    if (id == "map") {
        area.style.background = "url('static/img/space/boringSpace.jpg')";
        area.style.backgroundSize = "100% 100%";
        for(var i = 0; i < elems.length; i++) {
            elems[i].style.visibility = 'visible';
        }
        inven.style.visibility = 'hidden';
    } else if (id == "inventoryIcon") {
        if (inven.style.visibility == 'visible'){
            inven.style.visibility = 'hidden';
        } else {
            inven.style.visibility = 'visible';
        }
    } else {
        $.ajax({
            url: "/fuelCost",
            type: "POST",
            data: { location: id}
          }).done(function(data) {
              console.log(data);
             if (confirm("Do you want to travel to " + id + " for " + data.fuelCost)) {
                $.ajax({
                    url: "/travel",
                    type: "POST",
                    data: { location: id}
                  }).done(function(data) {
                      console.log(data);
                      if (data.code == 100) {
                        document.getElementById("currentFuel").innerHTML = data.fuel;
                        planetSelect(id);
                        currPlanet = id;
                      } else {
                          alert("Did not have enough fuel to travel");
                      }
                  });

            } else {

            }
          });

    }
}

function market() {
    var store = document.getElementById("store" + String(currPlanet));
    if (store.style.visibility == 'visible'){
        store.style.visibility = 'hidden';
    } else {
        store.style.visibility = 'visible';
    }

}

function planetSelect(id) {
    var area = document.getElementById("planetArea");
    var name = document.getElementById("currWorld");
    var elems = document.getElementsByClassName('planet');
    area.style.background = "url('static/img/planetBacks/" + id + ".jpg')";
    area.style.backgroundSize = "100% 100%";
    name.innerHTML = id;
    for(var i = 0; i < elems.length; i++) {
        elems[i].style.visibility = 'hidden';
    }
}

function end() {
    fuelErrorBox.style.visibility = 'hidden';
}

function fuelError() {
    confirmBox.style.visibility = 'hidden';
    fuelErrorBox.style.visibility = 'visible';
}

function okay(fuel, fuelReq) {
    console.log(fuel);
    console.log(fuelReq);
    if (fuel < fuelReq){
        fuelError();
    } else {
        document.getElementById("currentFuel").innerHTML = fuel - fuelReq;
        planetSelect(currPlanet);
    }

}

function buy(id, region) {
    $.ajax({
        url: "/buy",
        type: "POST",
        data: { name: id, region: region}
      }).done(function(data) {
          console.log(data);
          document.getElementById('credits').innerHTML = data.credit;
          document.getElementById('currentCargo').innerHTML = data.cargo_size;
          $('#inventory').empty();
          $("#inventory").append(
            "<tr>" +
              "<td>Item</td>" +
            "</tr>"
          );
          for(item in data.cargo) {
              $("#inventory").append(
                "<tr>" +
                  "<td>" + data.cargo[item] +"</td>" +
                "</tr>"
            );
          }

          alert(data.message);
      });
}

function sell(id, region) {
    $.ajax({
        url: "/sell",
        type: "POST",
        data: { name: id, region: region}
      }).done(function(data) {
          console.log(data);
          document.getElementById('credits').innerHTML = data.credit;
          document.getElementById('currentCargo').innerHTML = data.cargo_size;
          $('#inventory').empty();
          $("#inventory").append(
            "<tr>" +
              "<td>Item</td>" +
            "</tr>"
          );
          for(item in data.cargo) {
              $("#inventory").append(
                "<tr>" +
                  "<td>" + data.cargo[item] +"</td>" +
                "</tr>"
            );
          }

          alert(data.message);
      });
}
