$(function() {
   var conn = null;
   var name = "Unknown";
   var chName = window.location.pathname.slice(1);
   $('#channel').text(chName);
   function to_chat(msg) {
     var control = $('#log');
     control.html(control.html() + msg + '<br/>');
     control.scrollTop(control.scrollTop() + 1000);
   }
   function make_msg(msg) {
     var date = new Date();
     var date_prompt = '(' + date.toISOString().split('T')[1].slice(0,5) + ') ';
     var whole_msg = date_prompt + msg
     return whole_msg;
   }
   function connect() {
     disconnect();
     var wsUri = 'ws://localhost:5000/' + chName;
     conn = new WebSocket(wsUri);
     conn.onopen = function() {
       update_ui();
     };
     conn.onmessage = function(e) {
       var data = JSON.parse(e.data);
       switch (data.action) {
         case  'connect':
           name = data.name;
           var msgs = data.msgs;
           to_chat("(Connected as " + name + ")");
           to_chat("~~~Recent history beginning~~~");
           for(var i = 0; i < msgs.length; i++) {
              to_chat(msgs[i]);
           }
           to_chat("~~~~~Recent history end~~~~~");
           update_ui();
           break;
         case 'sent':
           to_chat(data.msg);
           break;
       }
     };
     conn.onclose = function() {
       conn = null;
       update_ui();
     };
   }
   function disconnect() {
     if (conn != null) {
       to_chat("(Disconnected)");
       conn.close();
       conn = null;
       name = 'Unknown';
       update_ui();
     }
   }
   function update_ui() {
     if (conn == null) {
       $('#status').text('Status: disconnected');
       $('#connect').html('Connect');
       $('#send').prop("disabled", true);
     } else {
       $('#status').text('Status: connected');
       $('#connect').html('Disconnect');
       $('#send').prop("disabled", false);
     }
     $('#name').text("Your name: " + name);
   }
   $('#connect').on('click', function() {
     if (conn == null) {
       connect();
     } else {
       disconnect();
     }
     update_ui();
     return false;
   });
   $('#send').on('click', function() {
     var text = $('#text').val();
     conn.send(make_msg(name + ": " + text));
     $('#text').val('').focus();
     return false;
   });
   $('#text').on('keyup', function(e) {
     if (e.keyCode === 13) {
       $('#send').click();
       return false;
     }
   });
 });