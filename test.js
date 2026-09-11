const fs = require('fs');
const content = fs.readFileSync('/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/frontend/src/components/ReportDetailModal.jsx', 'utf8');
console.log(content.includes('null.')); // check for obvious bad deref
