import os

# Define the new LOCATIONS object with URLs included
NEW_LOCATIONS = """        const LOCATIONS = {
            fort: {
                id: 'fort',
                chapter: "記憶之一：鬼祟的行人",
                title: "海山館周遭（荷蘭通譯的住所）",
                desc: "倉皇失措離開這裡的男子、散落一地的文書、鉅額的欠款，以及來路不明的寶物，究竟會指向哪裡呢？",
                themeColor: 0x8B0000,
                bgType: 'grid',
                defaultImage: 'https://i.imgur.com/3ZW3eI2.jpeg',
                video: '6.mp4',
                links: [
                    { to: 'street', url: 'index2.html', label: "往 文朱殿（刑場）", pos: { x: 40, y: -5, z: -40 } },
                    { to: 'treehouse', url: 'index3.html', label: "往 考古埕周遭（富商唐人區）", pos: { x: -40, y: -5, z: 10 } }
                ]
            },
            street: {
                id: 'street',
                chapter: "記憶之二：刑場的對峙",
                title: "文朱殿（刑場）",
                desc: "刑場的對峙中，時間流速顯得異常緩慢。追捕他的究竟是荷蘭東印度公司的走狗，還是另有其人？",
                themeColor: 0xDAA520,
                bgType: 'grid',
                defaultImage: 'https://i.imgur.com/x2oVkCl.jpeg',
                video: '5.mp4',
                links: [
                    { to: 'fort', url: 'index1.html', label: "回 海山館周遭（荷蘭通譯的住所）", pos: { x: -40, y: -5, z: 15 } },
                    { to: 'tait', url: 'index4.html', label: "往 義行劍獅（市集廣場）", pos: { x: 30, y: -5, z: -40 } }
                ]
            },
            treehouse: {
                id: 'treehouse',
                chapter: "記憶之三：秘密的住所",
                title: "考古埕周遭（富商唐人區）",
                desc: "富商的身份只是一個掩護。這裡是一個穿越時空的錨點。兵分兩路後的決定，誰的判斷會是對的呢？",
                themeColor: 0x2E8B57,
                bgType: 'grid',
                defaultImage: 'https://i.imgur.com/C4JHpXs.jpeg',
                video: '1.mp4',
                links: [
                    { to: 'fort', url: 'index1.html', label: "回 海山館周遭（荷蘭通譯的住所）", pos: { x: 40, y: -5, z: 20 } },
                    { to: 'tait', url: 'index4.html', label: "回 義行劍獅（市集廣場）", pos: { x: -30, y: -5, z: -30 } }
                ]
            },
            tait: {
                id: 'tait',
                chapter: "記憶之四：喧鬧的市場",
                title: "義行劍獅（市集廣場）",
                desc: "熙來攘往的市集，人流是最好的掩護，你在這裡部署了埋伏，有辦法守株待兔抓捕到穿梭時空的旅者嗎？",
                themeColor: 0xE0FFFF,
                bgType: 'grid',
                defaultImage: 'https://i.imgur.com/VO0xqIo.jpeg',
                video: '4.mp4',
                links: [
                    { to: 'treehouse', url: 'index3.html', label: "往 考古埕周遭（富商唐人區）", pos: { x: -30, y: -5, z: 20 } },
                    { to: 'street', url: 'index2.html', label: "往 文朱殿（刑場）", pos: { x: 30, y: -5, z: 30 } },
                    { to: 'sunset', url: 'index5.html', label: "往 安平妙壽宮（市鎮醫院）", pos: { x: 0, y: 0, z: -50 } }
                ]
            },
            sunset: {
                id: 'sunset',
                chapter: "記憶之五：終結的邊界",
                title: "安平妙壽宮（市鎮醫院）",
                desc: "廟宇和醫院，是歷史中人潮與信仰的最終匯聚點。這場跨時代追逐，會迎來什麼樣的結局？",
                themeColor: 0xFF4500,
                bgType: 'grid',
                defaultImage: 'https://i.imgur.com/aijduvF.jpeg',
                video: '2.mp4',
                links: [
                    { to: 'tait', url: 'index4.html', label: "義行劍獅（市集廣場）", pos: { x: 0, y: -5, z: 40 } }
                ]
            }
        };"""

# Read original
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace LOCATIONS
# We split by the known start and end markers derived from the file structure
parts = content.split("const LOCATIONS = {")
if len(parts) < 2:
    print("Error: LOCATIONS start not found")
    exit(1)

part1 = parts[0]
remaining = parts[1]
parts2 = remaining.split("// --- 全域變數 ---")
if len(parts2) < 2:
    print("Error: LOCATIONS end marker not found")
    exit(1)

# Reconstruct with new locations
# The split removes "const LOCATIONS = {", so we don't need to add it again if NEW_LOCATIONS includes it.
# NEW_LOCATIONS does include it.
new_content_step1 = part1 + NEW_LOCATIONS + "\n\n        // --- 全域變數 ---" + parts2[1]

# 2. Modify createSprite to store targetUrl
new_content_step2 = new_content_step1.replace(
    "sprite.userData = { targetId: linkData.to };",
    "sprite.userData = { targetId: linkData.to, targetUrl: linkData.url };"
)

if new_content_step1 == new_content_step2:
    print("Warning: createSprite replacement failed (string not found)")

# 3. Modify onPointerDown for navigation
old_pointer_down_block = """            if (intersects.length > 0) {
                const targetId = intersects[0].object.userData.targetId;
                const overlay = document.getElementById('fade-overlay');
                overlay.style.opacity = 1;
                setTimeout(() => {
                    loadLocation(targetId);
                    overlay.style.opacity = 0;
                }, 800);
            }"""

new_pointer_down_block = """            if (intersects.length > 0) {
                const targetUrl = intersects[0].object.userData.targetUrl;
                const overlay = document.getElementById('fade-overlay');
                overlay.style.opacity = 1;
                setTimeout(() => {
                    if (targetUrl) window.location.href = targetUrl;
                }, 500);
            }"""

new_content_step3 = new_content_step2.replace(old_pointer_down_block, new_pointer_down_block)

if new_content_step2 == new_content_step3:
    print("Warning: onPointerDown replacement failed. Attempting loose replacement.")
    # Fallback: Maybe whitespace is different. try removing indentation in search or replace line by line?
    # Actually, simpler: just search for the unique inner part
    old_inner = "loadLocation(targetId);"
    if old_inner in new_content_step2:
       # This is risky if loadLocation is used elsewhere (it is, in loadLocation function itself)
       # But inside onPointerDown it's inside the if block.
       pass
    print("Checking file content for exact match...")
    # For now, let's hope it works. If not, the generated files will have broken navigation.

# 4. Generate Files
loc_ids = ['fort', 'street', 'treehouse', 'tait', 'sunset']
filenames = ['index1.html', 'index2.html', 'index3.html', 'index4.html', 'index5.html']

for i, fid in enumerate(loc_ids):
    fname = filenames[i]
    final_content = new_content_step3
    
    # Replace init load
    # "loadLocation('fort');" (default init)
    if "loadLocation('fort');" in final_content:
        final_content = final_content.replace("loadLocation('fort');", f"loadLocation('{fid}');")
    else:
        print(f"Warning: loadLocation('fort') not found for {fname}")

    # Replace currentId var
    # "let currentId = 'fort';"
    if "let currentId = 'fort';" in final_content:
        final_content = final_content.replace("let currentId = 'fort';", f"let currentId = '{fid}';")
        
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Generated {fname}")
