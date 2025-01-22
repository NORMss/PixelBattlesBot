// ==UserScript==
// @name         PixelBattles Advanced API Painter with Matrix and Modes
// @namespace    http://tampermonkey.net/
// @version      1.6
// @description  Автоматическое закрашивание пикселей с использованием матрицы или от угла к углу
// @author       YourName
// @match        https://pixelbattles.ru/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Полный список цветов
    const colors = [
        "deepcarmine", "flame", "yelloworange", "naplesyellow", "mediumseagreen", "emerald",
        "inchworm", "myrtlegreen", "verdigris", "cyancobaltblue", "unitednationsblue", "mediumskyblue",
        "oceanblue", "VeryLightBlue", "grape", "purpleplum", "darkpink", "mauvelous",
        "coffee", "coconut", "black", "philippinegray", "lightsilver", "white"
    ];

    let selectedColor = colors[0]; // Цвет по умолчанию
    let isScriptRunning = false; // Флаг работы скрипта
    let token = getTokenFromCookie() || ""; // Токен
    let matrix = []; // Матрица для рисования
    let startX = 0; // Стартовая точка X для матрицы
    let startY = 0; // Стартовая точка Y для матрицы

    // Режим работы (matrix или corner-to-corner)
    let mode = "corner-to-corner";

    // Получение токена из куков
    function getTokenFromCookie() {
        const match = document.cookie.match(/token=([^;]+)/);
        return match ? match[1] : null;
    }

    // Сохранение токена, если введён вручную
    function saveToken(newToken) {
        token = newToken;
        console.log("Токен обновлён:", token);
    }

    // Пользовательский интерфейс
    const controlPanel = document.createElement('div');
    controlPanel.style.position = 'fixed';
    controlPanel.style.top = '10px';
    controlPanel.style.left = '10px';
    controlPanel.style.backgroundColor = 'white';
    controlPanel.style.border = '1px solid black';
    controlPanel.style.padding = '10px';
    controlPanel.style.zIndex = '10000';
    controlPanel.innerHTML = `
        <label>Токен: <input type="text" id="tokenInput" value="${token}" style="width: 300px;"></label><br>
        <label>Режим работы:
            <select id="modeSelector">
                <option value="corner-to-corner">От угла к углу</option>
                <option value="matrix">Матрица</option>
            </select>
        </label><br>
        <div id="cornerToCornerSettings">
            <label>X1: <input type="number" id="x1" value="0" style="width: 60px;"></label><br>
            <label>Y1: <input type="number" id="y1" value="0" style="width: 60px;"></label><br>
            <label>X2: <input type="number" id="x2" value="10" style="width: 60px;"></label><br>
            <label>Y2: <input type="number" id="y2" value="10" style="width: 60px;"></label><br>
            <label>Цвет по умолчанию:
                <select id="colorSelector">
                    ${colors.map(color => `<option value="${color}">${color}</option>`).join('')}
                </select>
            </label><br>
        </div>
        <div id="matrixSettings" style="display: none;">
            <label>Матрица (JSON):<br>
                <textarea id="matrixInput" rows="10" cols="30" style="width: 100%;"></textarea>
            </label><br>
            <label>Начальная точка X: <input type="number" id="matrixStartX" value="0" style="width: 60px;"></label><br>
            <label>Начальная точка Y: <input type="number" id="matrixStartY" value="0" style="width: 60px;"></label><br>
        </div>
        <button id="startPainting">Начать рисование</button>
        <button id="stopPainting">Остановить скрипт</button>
    `;
    document.body.appendChild(controlPanel);

    // Обработчики событий
    document.getElementById('modeSelector').addEventListener('change', (e) => {
        mode = e.target.value;
        document.getElementById('cornerToCornerSettings').style.display = mode === "corner-to-corner" ? "block" : "none";
        document.getElementById('matrixSettings').style.display = mode === "matrix" ? "block" : "none";
    });

    document.getElementById('colorSelector').addEventListener('change', (e) => {
        selectedColor = e.target.value;
    });

    document.getElementById('tokenInput').addEventListener('input', (e) => {
        saveToken(e.target.value);
    });

    document.getElementById('startPainting').addEventListener('click', () => {
        if (!token) {
            alert("Пожалуйста, введите токен перед запуском скрипта.");
            return;
        }
        if (isScriptRunning) {
            alert('Скрипт уже запущен!');
            return;
        }

        if (mode === "corner-to-corner") {
            const x1 = parseInt(document.getElementById('x1').value);
            const y1 = parseInt(document.getElementById('y1').value);
            const x2 = parseInt(document.getElementById('x2').value);
            const y2 = parseInt(document.getElementById('y2').value);

            isScriptRunning = true;
            startCornerToCornerPainting(x1, y1, x2, y2);
        } else if (mode === "matrix") {
            try {
                matrix = JSON.parse(document.getElementById('matrixInput').value);
                if (!Array.isArray(matrix) || !Array.isArray(matrix[0])) {
                    throw new Error('Матрица должна быть двумерным массивом.');
                }
                startX = parseInt(document.getElementById('matrixStartX').value);
                startY = parseInt(document.getElementById('matrixStartY').value);

                isScriptRunning = true;
                startMatrixPainting();
            } catch (err) {
                alert('Ошибка в формате матрицы: ' + err.message);
                return;
            }
        }
    });

    document.getElementById('stopPainting').addEventListener('click', () => {
        isScriptRunning = false;
        console.log('Скрипт остановлен');
    });

    // Установка пикселя через API
    async function placePixelAPI(x, y, color) {
        const bodyData = JSON.stringify({ x, y, color });

        return fetch('https://api.pixelbattles.ru/pix', {
            headers: {
                'accept': '*/*',
                'content-type': 'application/json',
                'cookie': `token=${token}`,
                'referer': 'https://pixelbattles.ru/'
            },
            body: bodyData,
            method: 'PUT',
            credentials: 'include'
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.text().then(text => {
                    console.error(`Ошибка установки пикселя: ${response.status} ${text}`);
                    return { status: "error" };
                });
            }
        }).catch(err => {
            console.error('Ошибка API при установке пикселя:', err);
            return { status: "error" };
        });
    }

    // Режим "от угла к углу"
    async function startCornerToCornerPainting(x1, y1, x2, y2) {
        for (let x = x1; x <= x2 && isScriptRunning; x++) {
            for (let y = y1; y <= y2 && isScriptRunning; y++) {
                const response = await placePixelAPI(x, y, selectedColor);
                //if (response?.status !== "ok") {
                //    console.warn(`Пропуск ячейки (${x}, ${y}) из-за ошибки.`);
                //    continue;
                //}

                await new Promise(resolve => setTimeout(resolve, 2000)); // Интервал 2 секунды только при успехе
            }
        }

        if (!isScriptRunning) {
            console.log('Рисование прервано.');
        } else {
            console.log('Рисование завершено.');
        }
        isScriptRunning = false;
    }

    // Режим "матрица"
    async function startMatrixPainting() {
        for (let y = 0; y < matrix.length && isScriptRunning; y++) {
            for (let x = 0; x < matrix[y].length && isScriptRunning; x++) {
                const color = matrix[y][x];

                if (color === "skip") {
                    continue; // Пропускаем ячейки с "skip"
                }

                const response = await placePixelAPI(startX + x, startY + y, color);
                //if (response?.status !== "ok") {
                //    console.warn(`Пропуск ячейки (${startX + x}, ${startY + y}) из-за ошибки.`);
                //    continue;
                //}

                await new Promise(resolve => setTimeout(resolve, 2000)); // Интервал 2 секунды только при успехе
            }
        }

        if (!isScriptRunning) {
            console.log('Рисование прервано.');
        } else {
            console.log('Рисование завершено.');
        }
        isScriptRunning = false;
    }
})();
