const input = document.getElementById('image-input');
const preview = document.getElementById('preview');
const result = document.getElementById('result');
const form = document.getElementById('upload-form');

input.addEventListener('change', () => {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    preview.src = e.target.result;
    preview.style.display = 'block';
  };
  reader.readAsDataURL(file);
});

// 表單送出後，顯示伺服器回傳的效果圖
form.addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(form);

  const resp = await fetch('/', {
    method: 'POST',
    body: formData
  });
  if (!resp.ok) {
    alert('辨識失敗');
    return;
  }
  const blob = await resp.blob();
  result.src = URL.createObjectURL(blob);
  result.style.display = 'block';
});
