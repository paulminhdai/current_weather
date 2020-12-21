console.log('Its working')
setTheme()
console.log('init')

var form = document.querySelector(".search");
form.addEventListener('submit', function(ev){
    setTheme();
    console.log('search...')
    return false;
});

function setTheme(){
    var date = new Date();
    var hour = date.getHours()
    //var hour = Math.floor(Math.random() * 25);
    console.log(hour)

    if (hour > 5 && hour < 17) {
        document.getElementById('theme-style').href='../static/styles/am.css';
    }
    else {
        document.getElementById('theme-style').href='../static/styles/pm.css';
    }
}
