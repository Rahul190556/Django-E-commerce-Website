//responsive slider using owl-carousel
$(document).ready(function() {
  $('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
        nav: false,
        autoplay: true
      },
      600: {
        items: 2,
        nav: true,
        autoplay: true
      },
      1000: {
        items: 4,
        nav: true,
        loop: true,
        autoplay: true
      }
      
    }
  });
});


// ajax in jQuery

  $('.plus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml=this.parentNode.children[2]
    console.log(id);
    $.ajax({
      type: 'GET',
      url: '/pluscart/',
      data: {
        prod_id: id
      },
      success: function(data) {
        // console.log(data);
        eml.innerText=data.quantity
        document.getElementById('amount').innerText=data.amount
        document.getElementById('totalamount').innerText=data.totalamount
      }
    });
  });


 $('.minus-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml=this.parentNode.children[2]
    // console.log(id);

    $.ajax({
      type: 'GET',
      url: '/minuscart/',
      data: {
        prod_id: id
      },
      success: function(data) {
        // console.log(data);
        eml.innerText=data.quantity
        document.getElementById('amount').innerText=data.amount
        document.getElementById('totalamount').innerText=data.totalamount
      }
    });
  });

 $('.remove-cart').click(function() {
    var id = $(this).attr('pid').toString();
    var eml=this
    console.log(id);
    
    $.ajax({
      type: 'GET',
      url: '/removecart/',
      data: {
        prod_id: id
      },
      success: function(data) {
        // console.log(data);
        document.getElementById('amount').innerText=data.amount
        document.getElementById('totalamount').innerText=data.totalamount
        document.getElementById('total_item').innerText=data.total_item
        eml.parentNode.parentNode.parentNode.parentNode.remove()
      }
    });
  });