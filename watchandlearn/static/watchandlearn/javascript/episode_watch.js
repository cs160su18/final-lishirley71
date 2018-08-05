var tag = document.createElement('script');
tag.id="iframe";
tag.src="https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('vid', {
      events: {
        'onReady': onPlayerReady
      }
    });      
}

function onPlayerReady(event){
  event.target.playVideo();
  function updateTime() {
      var videotime = 0;
    if(player && player.getCurrentTime) {
      videotime = player.getCurrentTime();

      console.log("time: "+Math.round(videotime));
        
        if(Math.round(videotime)==206){
            $("#popup").css("opacity","1");
        }
        
        $("#popup").click(function(){
            $("#tip").css("opacity","1");
        })
    }
  }
  timeupdater = setInterval(updateTime, 100);
}