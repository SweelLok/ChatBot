function openNav() {
	document.getElementById("myNavbar").style.width = "250px";
	document.getElementById("main").classList.add("shifted");
}

function closeNav() {
	document.getElementById("myNavbar").style.width = "0";
	document.getElementById("main").classList.remove("shifted");
}