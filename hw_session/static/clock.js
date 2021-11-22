function timeSet(){

    const twoDigit = (number) => {
        if (number < 10){
            number = "0" + number
        }
        return number
    }

    const base12 = (hour) => {
        if (hour % 12 == 0){
            return 12;
        }
        return hour % 12;
    }

    let currentDate = new Date();
    let month = document.getElementById("month");
    month.innerHTML = (currentDate.getMonth() +1) + " /";

    let day = document.getElementById("day");
    day.innerHTML = currentDate.getDate() + " /";

    let year = document.getElementById("year");
    year.innerHTML = currentDate.getFullYear();

    let hours = document.getElementById("hour");
    let hour = currentDate.getHours();
    hours.innerHTML = base12(hour) + " :";

    let minutes = document.getElementById("minutes");
    let mins = currentDate.getMinutes();
    minutes.innerHTML = twoDigit(mins);
    minutes.innerHTML = twoDigit(mins) + " :";

    let seconds = document.getElementById("seconds");
    let sec = currentDate.getSeconds();
    seconds.innerHTML = twoDigit(sec);
};
timeSet();
setInterval(timeSet, 1000);