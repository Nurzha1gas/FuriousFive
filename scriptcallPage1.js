// Объявление переменных
let APP_ID = "b52fae9e9d93464f996dc9ba1271b26d";
let token = null;
let uid = String(Math.floor(Math.random() * 10000));

let client;
let channel;

let localStream;
let remoteStream;
let peerConnection;

// Серверы ICE для установления соединения
const servers = {
    iceServers: [
        {
            urls: ['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302']
        }
    ]
};

let pendingCandidates = [];


let isMicrophoneOn = true; // Переменная для отслеживания состояния микрофона

// Функция для переключения микрофона
let toggleMicrophone = async () => {
    isMicrophoneOn = !isMicrophoneOn;
    let microphoneTrack = localStream.getTracks().find(track => track.kind === 'audio');
    if (microphoneTrack) {
        microphoneTrack.enabled = isMicrophoneOn;
    }

    // Изменение цвета кнопки микрофона
    let microphoneButton = document.getElementById('microphoneButton');
    microphoneButton.style.backgroundColor = isMicrophoneOn ? '#4CAF50' : '#FF5733'; // Зеленый когда включен, красный когда выключен
};
      
// Состояние камеры
let isCameraOn = true;

// Функция инициализации
let init = async () => {
    client = await AgoraRTM.createInstance(APP_ID);
    await client.login({ uid, token });

    channel = client.createChannel('main');
    await channel.join();

    channel.on('MemberJoined', handleUserJoined);
    client.on('MessageFromPeer', handleMessageFromPeer);

    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById('user-1').srcObject = localStream;

    // Привязка функции toggleCamera к кнопке камеры и toggleMicrophone к кнопке микрофона
    document.getElementById('cameraButton').addEventListener('click', toggleCamera);
    document.getElementById('microphoneButton').addEventListener('click', toggleMicrophone);
};

// Обработчик присоединения пользователя
let handleUserJoined = async (MemberId) => {
    console.log('A new user joined the channel:', MemberId);
    createOffer(MemberId);
};

// Обработчик сообщений от пиров
let handleMessageFromPeer = async (message, MemberId) => {
    try {
        let parsedMessage = JSON.parse(message.text);

        if (parsedMessage.type === 'offer') {
            await createAnswer(MemberId, parsedMessage.offer);
        } else if (parsedMessage.type === 'answer') {
            await addAnswer(parsedMessage.answer);
        } else if (parsedMessage.type === 'candidate') {
            await addIceCandidate(parsedMessage.candidate);
        }
    } catch (error) {
        console.error('Failed to handle message from peer:', error);
    }
};


// Создание соединения с пиром
let createPeerConnection = async (MemberId) => {
    peerConnection = new RTCPeerConnection(servers);

    remoteStream = new MediaStream();
    document.getElementById('user-2').srcObject = remoteStream;

    if (!localStream) {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        document.getElementById('user-1').srcObject = localStream;
    }

    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    });

    peerConnection.ontrack = (event) => {
        event.streams[0].getTracks().forEach((track) => {
            remoteStream.addTrack(track);
        });
    };

    peerConnection.onicecandidate = async (event) => {
        if (event.candidate) {
            client.sendMessageToPeer({ text: JSON.stringify({ 'type': 'candidate', 'candidate': event.candidate }) }, MemberId);
        }
    };
};


// Создание предложения соединения
let createOffer = async (MemberId) => {
    await createPeerConnection(MemberId);

    let offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);

    client.sendMessageToPeer({ text: JSON.stringify({ 'type': 'offer', 'offer': offer }) }, MemberId);
};

let createAnswer = async (MemberId, offer) => {
    await createPeerConnection(MemberId);

    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));

    let answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);

    client.sendMessageToPeer({ text: JSON.stringify({ 'type': 'answer', 'answer': answer }) }, MemberId);
};

let addAnswer = async (answer) => {
    if (peerConnection && !peerConnection.currentRemoteDescription) {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
        pendingCandidates.forEach(candidate => {
            peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
        });
        pendingCandidates = [];
    }
};

let addIceCandidate = async (candidate) => {
    if (peerConnection && peerConnection.remoteDescription) {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    } else {
        pendingCandidates.push(candidate);
    }
};


// Функция для переключения камеры
let toggleCamera = async () => {
    if (localStream) {
        isCameraOn = !isCameraOn;
        let videoTrack = localStream.getTracks().find(track => track.kind === 'video');
        if (videoTrack) {
            videoTrack.enabled = isCameraOn;
        }
    }

    // Изменение цвета кнопки камеры
    let cameraButton = document.getElementById('cameraButton');
    cameraButton.style.backgroundColor = isCameraOn ? '#4CAF50' : '#FF5733'; // Зеленый когда включен, красный когда выключен
};


// Инициализация приложения
init();
