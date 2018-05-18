export function MP () {  
  return new Promise(function (resolve, reject) {
    window.onload = () => {
      resolve(BMap)
    }
    var script = document.createElement("script")
    script.type = "text/javascript"
    script.src = "http://api.map.baidu.com/api?v=2.0&ak=9QDEhrhgyE9sucnUWcKsQGATp1al2Mvx&callback=init"
    script.onerror = reject

    document.head.appendChild(script)
  })  
}  