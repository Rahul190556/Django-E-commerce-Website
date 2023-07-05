window.addEventListener("load",()=>{
    const loader=document.querySelector(".loader");

    setTimeout(() => {
        loader.classList.add("loader-hidden");
    }, 500);

    loader.addEventListener("transitionend",()=>{
        document.body.removeChild(loader);
    });
})