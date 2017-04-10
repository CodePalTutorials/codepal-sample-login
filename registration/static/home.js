/**
 * Created by shivam on 4/8/17.
 */

 var facebookAppId = '282341848860029';
//var facebookAppId = '283099212117626';

/* Initializes facebook SDk.
* */
function initFB () {
    (function (d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s);
        js.id = id;
        js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId="+facebookAppId;
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
    }

 /* Logs In to facebook. Registers user if login is success
* */
function loginFacebook() {
    FB.init({
    appId:facebookAppId,
    cookie:true,
    status:true,
    xfbml:false
    });

    FB.login(function(response) {

      if (response.status === 'connected') {
        // Logged into your app and Facebook.
        onFacebookLoginSuccess(response.authResponse);
      } else {
        // The person is not logged into this app or we are unable to tell.
          onLoginFaliure();
      }
    },  {scope: 'email'});

    }

    function onLoginFaliure(){
        // Display an error toast,\
        toastr.error('Please try again', 'Login Failed!')
    }

    function onFacebookLoginSuccess(facebookResponse){
        var jqxhr = $.ajax({
            type: 'POST',
            url: 'api/v1/user/register/facebook',
            data: JSON.stringify(facebookResponse),
            dataType: 'text',
            contentType: 'application/json; charset=utf-8',
            xhrFields: {
               withCredentials: true
            },
           crossDomain: true,
            beforeSend: function(xhr){
               xhr.withCredentials = true;
            }
        });


        jqxhr.done(function(data, textStatus, jqXHR) {
            toastr.success('Logged In successfully!', 'Success')
        });

        jqxhr.fail(function(jqXHR, textStatus, errorThrown) {
            toastr.error('Please try again', 'Login Failed!')
        });

    }

    function fetch_and_update_profile() {

        var jqxhr = $.ajax({
            type: 'GET',
            url: 'api/v1/user/get/account',
            dataType: 'text',
            contentType: 'application/json; charset=utf-8',
            xhrFields: {
               withCredentials: true
            },
           crossDomain: true,
            beforeSend: function(xhr){
               xhr.withCredentials = true;
            }
        });


        jqxhr.done(function(data, textStatus, jqXHR) {
            toastr.success('Details Fetched successfully!', 'Success');
            var response = JSON.parse(data);
              $( ".text-name" ).text(response.name);
              $( ".text-email" ).text(response.email);
              $( "#photo" ).attr('src', 'http://graph.facebook.com/'+response.facebook_id+'/picture?type=large')
        });

        jqxhr.fail(function(jqXHR, textStatus, errorThrown) {
            toastr.error('You are not allowed to make that request. Sign up first', 'Not authorized!');
        });

    }


    function initButtons(){

        $( "#btn-facebook-signin" ).click(function() {
          loginFacebook();
        });

        $( "#btn-fetch-profile" ).click(function() {
            fetch_and_update_profile();
        });
    }


    window.onload = function() {
        initFB();
        initButtons();
    };