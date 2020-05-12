$(document).ready(function(){
    // Contact
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")


    function displaySubmition(submitBtn, submitText, doSubmit ){
        if (doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Submiting..")
        }
        else{
            submitBtn.removeClass("disabled")
            submitBtn.html(submitText)
        }
        
    }
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        var contactFormBtn = contactForm.find("[type ='submit']")
        var contactFormBtnText = contactFormBtn.text()
        //var thisForm = $(this)
        displaySubmition(contactFormBtn, "", true)
        $.ajax({
            url: contactFormEndpoint,
            method: contactFormMethod,
            data : contactFormData,
            success:function(data){
                //thisForm.reset()
                console.log(contactForm)
                contactForm[0].reset()
                
                setTimeout(function(){
                    displaySubmition(contactFormBtn, contactFormBtnText, false)
                }, 500)
                $.alert({
                    title : "Success",
                    content : data.message,
                    theme : "modern"
                })
            },
            error: function(error){ 
                console.log(error)
                var errorMsg = error.responseJSON
                var msg = ""
                $.each(errorMsg, function(key,value){
                    msg += key + ": "+ value[0].message+ "<br/>"
                })
                
                setTimeout(function(){
                    displaySubmition(contactFormBtn, contactFormBtnText, false)
                }, 500)
                $.alert({
                    title: "Oops",
                    content :msg,
                    theme : "modern"
                })
            }
        })
    })


    // Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer ;
    var typingInterval = 1500
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch,typingInterval)
    })
    
    searchInput.keydown(function(event){
        // key pressend
        clearTimeout(typingTimer)
    })

    function displaySearching(){
        searchBtn.addClass("disabled")
        // or the spinner instead <i class='fa fa-spin fa-spinner'
        searchBtn.html("<i class='fa fa-spin fa-circle-notch'></i>Searching...")
       
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href='/search/?q=' + query
        },1000)
        
    }

    // Cart and Products
    var productForm = $(".form_product_ajax")
    productForm.submit(function(event){
        event.preventDefault();
        console.log("Form is not sending")
        var thisForm=$(this)
        //var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
        $.ajax({
            url:actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                /* console.log("success")
                console.log(data) */
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("<button class='btn btn-warning' type='submit'>Remove from Cart</button>")
                    console.log("added ",data.added)
                    console.log("remove", data.removed)
                } else {
                    submitSpan.html("<button class='btn btn-primary' type='submit'>Add to cart</button>")
                    /* console.log("added", data.added)
                    console.log("remove", data.removed) */
                }
                var navbarCount = $(".navbar_count")
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") !=1){
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Error",
                    content : "Sorry you can't add or remove",
                    theme : "modern"
                })
                /* console.log("error")
                console.log(errorData) */
            }
        })            
    })
    function refreshCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody  = cartTable.find(".cart-body")
        //cartBody.html("<h1>changed</h1>")
        var productsRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        var refreshCartUrl = "/api/cart/"
        var refreshCartMethod = "GET"
        var data = {}
        $.ajax({
            url : refreshCartUrl ,
            mehtod : refreshCartMethod,
            data : data,
            success :function(data){
                console.log("success")
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){
                    productsRows.html(" ")
                   i=data.products.length
                    $.each(data.products, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display","block")
                        // newCartItemRemove.removeClass("hidden-class")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">"
                        +i+"</th><td><a href='"+value.url+"'>"
                        +value.name+"</a>"+newCartItemRemove.html()+"</td><td>"+value.price+"</td></tr>")
                        i--
                    })
                    /* cartBody.prepend("<tr><th scope=\"row\">{{forloop.counter}}</th><td colspan=3>Coming soon</td></tr>") */
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
                
            },
            error : function(errorData){
                console.log("error")
                console.log(errorData)
            }
        })

    }
})