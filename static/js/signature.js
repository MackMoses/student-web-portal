// ==========================================================
// OFFICER SIGNATURE CANVAS
// ==========================================================

const signatureCanvas = document.getElementById("signature-pad");
const signatureCtx = signatureCanvas.getContext("2d");

// ==========================================================
// APPROVAL MARK CANVAS
// ==========================================================

const approvalCanvas = document.getElementById("approval-pad");
const approvalCtx = approvalCanvas.getContext("2d");

// ==========================================================
// DRAWING FLAGS
// ==========================================================

let drawingSignature = false;
let drawingApproval = false;

// ==========================================================
// GET MOUSE / TOUCH POSITION
// ==========================================================

function getPosition(e, canvas) {

    const rect = canvas.getBoundingClientRect();

    if (e.touches) {

        return {

            x: e.touches[0].clientX - rect.left,

            y: e.touches[0].clientY - rect.top

        };

    }

    return {

        x: e.clientX - rect.left,

        y: e.clientY - rect.top

    };

}

// ==========================================================
// START DRAWING
// ==========================================================

function startSignature(e) {

    drawingSignature = true;

    const pos = getPosition(e, signatureCanvas);

    signatureCtx.beginPath();

    signatureCtx.moveTo(pos.x, pos.y);

}

function startApproval(e) {

    drawingApproval = true;

    const pos = getPosition(e, approvalCanvas);

    approvalCtx.beginPath();

    approvalCtx.moveTo(pos.x, pos.y);

}

// ==========================================================
// DRAW
// ==========================================================

function drawSignature(e) {

    if (!drawingSignature) return;

    e.preventDefault();

    const pos = getPosition(e, signatureCanvas);

    signatureCtx.lineTo(pos.x, pos.y);

    signatureCtx.strokeStyle = "blue";

    signatureCtx.lineWidth = 2;

    signatureCtx.lineCap = "round";

    signatureCtx.stroke();

}

function drawApproval(e) {

    if (!drawingApproval) return;

    e.preventDefault();

    const pos = getPosition(e, approvalCanvas);

    approvalCtx.lineTo(pos.x, pos.y);

    approvalCtx.strokeStyle = "blue";

    approvalCtx.lineWidth = 2;

    approvalCtx.lineCap = "round";

    approvalCtx.stroke();

}

// ==========================================================
// STOP DRAWING
// ==========================================================

function stopSignature() {

    drawingSignature = false;

}

function stopApproval() {

    drawingApproval = false;

}

// ==========================================================
// SIGNATURE EVENTS
// ==========================================================

signatureCanvas.addEventListener("mousedown", startSignature);
signatureCanvas.addEventListener("mousemove", drawSignature);
signatureCanvas.addEventListener("mouseup", stopSignature);
signatureCanvas.addEventListener("mouseleave", stopSignature);

signatureCanvas.addEventListener("touchstart", startSignature);
signatureCanvas.addEventListener("touchmove", drawSignature);
signatureCanvas.addEventListener("touchend", stopSignature);

// ==========================================================
// APPROVAL EVENTS
// ==========================================================

approvalCanvas.addEventListener("mousedown", startApproval);
approvalCanvas.addEventListener("mousemove", drawApproval);
approvalCanvas.addEventListener("mouseup", stopApproval);
approvalCanvas.addEventListener("mouseleave", stopApproval);

approvalCanvas.addEventListener("touchstart", startApproval);
approvalCanvas.addEventListener("touchmove", drawApproval);
approvalCanvas.addEventListener("touchend", stopApproval);

// ==========================================================
// CLEAR SIGNATURE
// ==========================================================

document.getElementById("clear").onclick = function(e){

    e.preventDefault();

    signatureCtx.clearRect(

        0,

        0,

        signatureCanvas.width,

        signatureCanvas.height

    );

};

// ==========================================================
// CLEAR APPROVAL
// ==========================================================

document.getElementById("clearApproval").onclick = function(e){

    e.preventDefault();

    approvalCtx.clearRect(

        0,

        0,

        approvalCanvas.width,

        approvalCanvas.height

    );

};

// ==========================================================
// SAVE BOTH IMAGES
// ==========================================================

document.getElementById("save").onclick = function(e){

    e.preventDefault();

    document.getElementById("approval").value =

        approvalCanvas.toDataURL("image/png");

    document.getElementById("signature").value =

        signatureCanvas.toDataURL("image/png");

    document.getElementById("signatureForm").submit();

};