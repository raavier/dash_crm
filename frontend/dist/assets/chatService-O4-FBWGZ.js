import{a}from"./index-B-pk8tbj.js";class t{async sendMessage(e,s){return(await a.post("/api/chat/message",{user_id:e,query:s})).data}}const o=new t;export{o as chatService};
