function Tags(element) {
  var DOMParent = element;
  var DOMList;
  var DOMInput;
  var dataAttribute;
  var arrayOfList;

  function DOMCreate() {
    var ul = document.createElement("ul");
    DOMParent.appendChild(ul); // first child is <ul>

    DOMList = DOMParent.firstElementChild; // last child is <input>

  }

  function DOMRender() {
    // clear the entire <li> inside <ul>
    DOMList.innerHTML = ""; // render each <li> to <ul>

    arrayOfList.forEach(function (currentValue, index) {
      var li = document.createElement("li");
      li.innerHTML = "".concat(currentValue, '<a><i class="fas fa-times-circle"></i></a>');
      li.querySelector("a").addEventListener("click", function () {
        onDelete(index);
      });
      DOMList.appendChild(li);
    });
    setAttribute();
  }

  function onDelete(id) {
    arrayOfList = arrayOfList.filter(function (currentValue, index) {
      if (index === id) {
        return false;
      }

      return currentValue;
    });
    DOMRender();
  }

  function getAttribute() {
    dataAttribute = DOMParent.getAttribute("data-simple-tags");
    dataAttribute = dataAttribute.split(","); // store array of data attribute in arrayOfList

    arrayOfList = dataAttribute.map(function (currentValue) {
      return currentValue.trim();
    });
  }

  function setAttribute() {
    DOMParent.setAttribute("data-simple-tags", arrayOfList.toString());
  }

  getAttribute();
  DOMCreate();
  DOMRender();
} // run immediately


;

(function () {
  var DOMSimpleTags = document.querySelectorAll(".simple-tags");
  DOMSimpleTags = Array.from(DOMSimpleTags);
  DOMSimpleTags.forEach(function (currentValue) {
    // create Tags
    new Tags(currentValue);
  });
})();
