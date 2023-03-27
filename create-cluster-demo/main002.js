const div_ = () => document.createElement('div');
const form_ = () => document.createElement('form');
const label_ = () => document.createElement('label');
const input_ = () => document.createElement('input');
const table_ = () => document.createElement('table');
const tr_ = () => document.createElement('tr');
const td_ = () => document.createElement('td');
const p_ = () => document.createElement('p');
const a_ = () => document.createElement('a');

const name_list = [
    '火鸡', '高鸟', '猎犬', '兔叽', '猪猪', '蝴蝶', '鼹鼠', '海象', '鱼人', '龙蝇', '鹿鸭', '蚁狮', '熊獾', '巨鹿', '蛤蟆', '螃蟹',
    '蝾螈', '查理', '战车', '主教', '骑士', '蝙蝠', '乌鸦', '红雀', '雪雀', '鹦鹉', '浣猫', '兔子', '天体', '青蛙', '疯猪', '企欧',
    '雪兔', '电羊', '红象', '冬象', '触手', '座狼', '钢羊', '月蛾', '果蝇', '蜜蜂', '蜂后', '幽灵', '蚊子', '海草', '鲨鱼', '树精',
    '哈奇', '阿比', '伯尼', '猴子', '蜗牛', '石虾', '尘蛾', '犀牛', '树精', '鱿鱼', '龙虾', '鲸鱼', '克眼', '哨兵'
];
const boolean_val = {true: '开启', false: '关闭'};
const cluster_dataset = {
    code: {
        game_mode: {survival: '生存', endless: '无尽', wilderness: '荒野'},
        cluster_intention: {social: '社交', cooperative: '合作', competitive: '竞争', madness: '疯狂'},
        cluster_language: {
            zh: '汉语 简体',
            zht: '汉语 繁体',
            en: '英语',
            fr: '法语',
            es: '西班牙语',
            de: '德语',
            it: '意大利语',
            pt: '葡萄牙语',
            pl: '波兰语',
            ru: '俄语',
            ko: '韩语',
        },
        tick_rate: {'10': '10', '15': '15', '20': '20', '30': '30', '60': '60'},
        vote_enabled: boolean_val,
        console_enabled: boolean_val,
        pvp: boolean_val,
        pause_when_empty: boolean_val,
        autosaver_enabled: boolean_val,
        lan_only_cluster: boolean_val,
        offline_cluster: boolean_val,
        steam_group_only: boolean_val,
        steam_group_admins: boolean_val,
        shard_enabled: boolean_val,
        autocompiler_enabled: boolean_val,
        
    },
    list: {},
    default: {
        game_mode: 'survival',
        cluster_intention: 'cooperative',
        cluster_language: 'zh',
        tick_rate: '15',
        vote_enabled: 'true',
        console_enabled: 'true',
        pvp: 'false',
        pause_when_empty: 'true',
        autosaver_enabled: 'true',
        lan_only_cluster: 'false',
        offline_cluster: 'false',
        steam_group_only: 'false',
        steam_group_admins: 'false',
        shard_enabled: 'true',
        autocompiler_enabled: 'false',
        
        cluster_name: '一拳一个小' + name_list[Math.floor(Math.random() * name_list.length)],
        cluster_description: '',
        max_players: '6',
        cluster_password: ' ',
        idle_timeout: '1800',
        whitelist_slots: '0',
        override_dns: ' ',
        max_snapshots: '6',
        steam_group_id: ' ',
        bind_ip: '127.0.0.1',
        master_ip: '127.0.0.1',
        master_port: '10888',
        cluster_key: 'supersecretkey',
        connection_timeout: '8000',
    },
}
cluster_dataset.list = Object.fromEntries([...Object.entries(cluster_dataset.code)].map(n => [n[0], Object.keys(n[1])]));

(function init_cluster_input() {
    const form = document.getElementById('form_cluster');
    const input_list = [...form.getElementsByTagName('input'), ...form.getElementsByTagName('textarea')];
    for (let ele_input of input_list) {
        // 通用处理
        const name = ele_input.name;
        const placeholder = cluster_dataset.default[name];
        ele_input.placeholder = placeholder;
        
        if (!ele_input.readOnly) {
            continue;
        }
        const value_list = cluster_dataset.list[name];
        if (!value_list) {
            console.log('没有对应的键值列表', ele_input);
            continue;
        }
        // 处理带有键值列表的元素
        ele_input.placeholder = cluster_dataset.code[name][placeholder];
        const index = value_list.indexOf(placeholder);
        ele_input.dataset.index = index.toString();

        for (let [type, close, place] of [['pre', index === 0, 'beforebegin'], ['next', index === value_list.length - 1, 'afterend']]) {
            const ele_label = label_();
            ele_label.className = `label_change_value change_value_${type}`;
            ele_label.id = `${ele_input.id}_${type}`;
            ele_label.htmlFor = ele_input.id;
            if (close) {
                ele_label.onclick = null;
                ele_label.setAttribute('disabled', '');
            } else {
                ele_label.onclick = function () {
                    change_value(type, 'cluster', this);
                }
            }
            if (place === 'beforebegin') {
                ele_input.insertAdjacentElement(place, ele_label);  // 猪 ide，为什么乱报警告
            } else if (place === 'afterend') {
                ele_input.insertAdjacentElement(place, ele_label);  // 猪 ide，为什么乱报警告
            }
        }
    }
})();

(function enter_to_do() {
    const enter_event = {
        cluster_adminlist_raw: "cluster_adminlist_raw_button",
        cluster_whitelist_raw: "cluster_whitelist_raw_button",
        cluster_blacklist_raw: "cluster_blacklist_raw_button",
        mod_search_add: "mod_search",
    };
    
    const ele_input_list = [...document.getElementsByTagName('input'), ...document.getElementsByTagName('textarea')];
    ele_input_list.forEach(ele_input=>{
        if (ele_input.id in enter_event) {
            ele_input.addEventListener('keydown', (KeyboardEvent)=>{
                KeyboardEvent.key === "Enter" && document.getElementById(enter_event[ele_input.id]).click();
            });
            return;
        }
        ele_input.addEventListener('keydown', (KeyboardEvent)=>{
            KeyboardEvent.key === "Enter" && ele_input.blur();
        });
    });
})();


const world_dataset = {forest:{code: {}, list: {}, default: {}}, cave:{code: {}, list: {}, default: {}}}

let dst_world_obj = {0: {0: {}}};

const world_id_name = {};
const fix_world_name = {forest: 'Master', cave: 'Caves'};

const mod_info_saved = {}
const modinfo_dataset = {};
// {222222222: {opt1: {{dataset: [{description: '', data: ?, hover: ''}, ], default_index: '', hover: '', type: '', label: '', name: ''}}, opt2: {}}}

// 获取窗口高度
const getWindowHeight = (function () {
    if (window.innerHeight) {
        return function () {
            return window.innerHeight;
        };
    } else if (document.documentElement.clientHeight) {
        return function () {
            return document.documentElement.clientHeight;
        };
    } else if (document.body.clientHeight) {
        return function () {
            return document.body.clientHeight;
        };
    }
})();

// 获取窗口宽度
const getWindowWidth = (function () {
    if (window.innerWidth) {
        return function () {
            return window.innerWidth;
        };
    } else if (document.documentElement.clientWidth) {
        return function () {
            return document.documentElement.clientWidth;
        };
    } else if (document.body.clientWidth) {
        return function () {
            return document.body.clientWidth;
        };
    }
})();

getWindowWidth() && getWindowHeight();

// copy
const copy_text = (function () {
    if (navigator.clipboard) {
        return function (text) {
            navigator.clipboard.writeText(text).then(() => 'copy right').catch(() => 'copy wrong');
        }
    } else {
        window.ele_copyarea = document.createElement('textarea');
        ele_copyarea.style.width = '0';
        ele_copyarea.style.position = 'fixed';
        ele_copyarea.style.left = '-999px';
        ele_copyarea.style.top = '9px';
        ele_copyarea.tabIndex = -1;
        ele_copyarea.id = 'tempTextarea';
        return function (text) {
            document.body.appendChild(window.ele_copyarea);
            const ele_copyarea = document.getElementById('tempTextarea');
            ele_copyarea.value = text;
            ele_copyarea.select();
            document.execCommand('copy', true);
            document.body.removeChild(window.ele_copyarea);
        }
    }
})();

// copied_tip
const copy_right = function (text) {
    const emoji_button = document.getElementById('emoji_bar_button')
    emoji_button.value = text;
    emoji_button.classList.add('copy_right');
    setTimeout(function () {
        emoji_button.classList.remove('copy_right');
    }, 500);
};

//屏蔽 ctrl + +/- 缩放
document.addEventListener('keydown', function (event) {
    if ((event.ctrlKey || event.metaKey)
        && (event.key === "=" || event.key === "+" || event.key === "-")) {
        event.preventDefault();
    }
}, false);

//屏蔽 ctrl + 鼠标滚轮缩放
document.addEventListener('wheel', function (event) {
    if (event.ctrlKey || event.metaKey) {
        event.preventDefault();
    }
}, {
    capture: false,
    passive: false,
});

window.onresize = function () {
    // const width = getWindowWidth();
    // document.getElementById("html").style.fontSize = (width / 1280 * 1.25).toString() + 'vw'
    // alert(document.getElementById("html").style.fontSize)
    // alert(window.getComputedStyle(document.getElementById("test")).getPropertyValue("height") || "?");

};

let allow_press_time = 0;
const running_task = [];
const lastest_self = {}
function can_i_press(task_name, start_time) {
    if (running_task.includes(task_name)) {
        iam_running();
        return false;
    }
    lastest_self[task_name] = start_time;
    running_task.push(task_name);
    setTimeout(() => run_tried(task_name), 10000);
    
    if (Date.now() >= allow_press_time) {
        allow_press_time = Date.now() + 1000;
        return true;
    } else {
        dont_press();
        run_tried(task_name);
        return false;
    }
}

function run_tried(task_name) {
    const index = running_task.indexOf(task_name);
    if (index !== -1) {
        running_task.splice(index, 1);
    }
}

function dont_press() {
    alert('不要一直点');
}

function iam_running() {
    alert('别点，在忙');
}

function onload_1() {
    // chrome 限制最小窗口，因为最小字号 12px 影响显示
    // const width = getWindowWidth();
    // const screen_width = window.screen.width
    // document.getElementById("html").style.height = (720).toString() + 'px'
    // document.getElementById("html").style.width = (1264).toString() + 'px'
    // document.getElementById("html").style.fontSize = (width / 1280 * 10).toString() + 'px'

    // 遍历每个按钮为其添加点击事件
    for_show_button(document.getElementsByClassName("show_button"))
    // 为表情添加点击复制
    document.getElementById('emoji_bar_button').onclick = emoji_bar;
    for (let emoji_span of document.getElementsByClassName("emoji_item")) {
        emoji_span.addEventListener('click', function () {
                copy_text(this.textContent);
                copy_right(this.textContent);
            }
        )
    }

    get_world_json().then(r => {
        dst_world_obj = r['zh']

        update_world_info();

        add_world('forest', 'show')
        document.getElementById('content_placeholder').classList.remove('show');
        add_world('cave')
    });

}


function update_world_info() {
    for (let [world_name, world_obj] of Object.entries(dst_world_obj)) {
        if (!world_dataset[world_name]) {
            world_dataset[world_name] = {};
        }
        world_dataset[world_name].list = {};
        world_dataset[world_name].code = {};
        world_dataset[world_name].default = {};
        for (let group_obj of Object.values(world_obj)) {
            for (let item_obj of Object.values(group_obj)) {
                const items = item_obj['items'];
                const items_desc = item_obj['desc'];
                for (let [name, item] of Object.entries(items)) {
                    if (!world_dataset[world_name].code.hasOwnProperty(name)) {
                        const def = item['value'];
                        const desc = item['desc'] ?? items_desc;
                        world_dataset[world_name].list[name] = Object.keys(desc);
                        world_dataset[world_name].code[name] = desc;
                        world_dataset[world_name].default[name] = def;
                    }
                }
            }
        }
    }
}

function add_world(world_type, isshow = '') {
    const world_id_list = [...Object.keys(world_id_name)];
    const world_name_list = [...Object.values(world_id_name)];
    const forest_list = world_name_list.filter(n => n.startsWith(fix_world_name.forest));
    const cave_list = world_name_list.filter(n => n.startsWith(fix_world_name.cave));
    const world_id = 'world' + select_lack_min_num(world_id_list.map(n => {
        return +n.replace('world', '');
    }), world_id_list.length ? +world_id_list.at(-1) : 1);
    const data = {
        forest: {name: fix_world_name.forest, list: forest_list},
        cave: {name: fix_world_name.cave, list: cave_list}
    }[world_type];
    const num = select_lack_min_num(data.list.map(n => {
        const m = +n.replace(data.name, '');
        return (m === 0) ? 1 : m;
    }), 1);
    const world_name = data.name + ((num === 1) ? '' : num);
    world_id_name[world_id] = world_name;
    create_world_sider(world_id, world_name, world_type);
    create_world_item(world_id, world_name, world_type, isshow);
    create_mod_sider(world_id, world_name, world_type);
    create_mod_item(world_id, world_name, world_type, isshow);
    fix_world_info();
}


// [3, 4, 6, 7], start => [start, 3, 4, 6, 7] => start
function select_lack_min_num(value_list, start = null) {
    if (value_list.length === 0) {
        return +start;
    }
    value_list.sort((m, n) => m - n);
    start === null && (start = value_list[0])
    for (let value = start; value < value_list.at(-1) + 1; value++) {
        if (!value_list.includes(value)) {
            return value;
        }
    }
    return value_list.at(-1) + 1;
}

function del_world() {
    const world_id = this.id.replace('button_', '').replace('_del', '');
    const world_button = document.getElementById(this.id.replace('_del', ''));
    const world_button_div = this.parentElement;
    const world_content = document.getElementById(`content_${world_id}`);
    const mod_button = document.getElementById(`button_mod_${world_id}`);
    const mod_button_div = mod_button.parentElement;
    const mod_content = document.getElementById(`content_mod_${world_id}`);
    
    if (world_button.className.includes('active')) {
        const buttons = document.getElementById('world_sidebar').getElementsByClassName('world_sidebar_button')
        for (let btn of buttons) {
            if (btn.parentNode !== this.parentNode) {
                btn.click();
                break;
            }
        }
    }
    if (mod_button.className.includes('active')) {
        const buttons = document.getElementById('mod_sidebar').getElementsByClassName('world_sidebar_button')
        for (let btn of buttons) {
            if (btn.parentNode !== mod_button.parentNode) {
                btn.click();
                break;
            }
        }
    }
    world_content.remove();
    world_button_div.remove();
    mod_content.remove()
    mod_button_div.remove()
    delete world_id_name[world_id];
    fix_world_info();
}

function fix_world_info() {
    const world_id_list = [...Object.keys(world_id_name)];
    const input_name_list = ['id', 'name', 'is_master', 'server_port', 'encode_user_path', 'master_server_port', 'authentication_port'];
    const input_data = {};
    world_id_list.forEach(m => {
        input_data[m] = {};
        input_name_list.forEach(n => input_data[m][n] = document.getElementById(`button_${n}_${m}`));
    });
    let master_world_id;
    for (let is_master_input of [...Object.values(input_data)].map(n => n['is_master'])) {
        if (is_master_input.value) {
            master_world_id = is_master_input.id.replace('button_is_master_', '');
            break;
        }
    }
    if (!master_world_id) {
        master_world_id = 'world1';
    }
    const sec_world_id_list = world_id_list;
    sec_world_id_list.splice(sec_world_id_list.indexOf(master_world_id), 1);

    // is_master
    document.getElementById(`button_${master_world_id}_del`).classList.add('hidden');
    sec_world_id_list.forEach(world_id => {
        input_data[world_id]['is_master'].placeholder = '否';
        document.getElementById(`button_${world_id}_del`).classList.remove('hidden');
    });

    // sort sec_world_id_list > [master, [...forset], [...cave]]
    const [sec_forest_id_list, sec_cave_id_list] = [[], []];
    sec_world_id_list.forEach(n => {
        if (world_id_name[n].startsWith(fix_world_name.forest)) {
            sec_forest_id_list.push(n);
        } else if (world_id_name[n].startsWith(fix_world_name.cave)) {
            sec_cave_id_list.push(n);
        }
    });
    [sec_forest_id_list, sec_cave_id_list].forEach(list => list.sort((m, n) => m.slice(5) - n.slice(5)));
    const new_world_id_list = [master_world_id].concat(sec_forest_id_list).concat(sec_cave_id_list);

    // id, server_port, master_server_port, authentication_port
    const [server_port_obj, master_server_port_obj, authentication_port_obj] = [{}, {}, {}];
    new_world_id_list.forEach((world_id, index) => {
        const world_info = input_data[world_id];
        world_info['id'].placeholder = index + 1;
        +world_info['server_port'].value && (server_port_obj[world_id] = +world_info['server_port'].value);
        +world_info['master_server_port'].value && (master_server_port_obj[world_id] = +world_info['master_server_port'].value);
        +world_info['authentication_port'].value && (authentication_port_obj[world_id] = +world_info['authentication_port'].value);
    });

    const cluster_port_input = document.getElementById('button_master_port');
    const cluster_port = +(cluster_port_input.value || cluster_port_input.placeholder)
    const def_server_port = {0: 10999, 1: 10998, base: 10998};
    const modify_server_port = new_world_id_list.filter(world_id => !server_port_obj[world_id]);
    const def_master_server_port = {0: 27016, base: 27016};
    const modify_master_server_port = new_world_id_list.filter(world_id => !master_server_port_obj[world_id]);
    const def_authentication_port = {0: 8766, base: 8766};
    const modify_authentication_port = new_world_id_list.filter(world_id => !authentication_port_obj[world_id]);

    const port_value_list = [cluster_port, ...Object.values(server_port_obj), ...Object.values(master_server_port_obj), ...Object.values(authentication_port_obj)]

    if (this.tagName === 'INPUT') {
        const this_value = +this.value
        if (port_value_list.indexOf(this_value) !== port_value_list.lastIndexOf(this_value)) {
            this.value = '';
            tip('与已填写的其它端口重复');
        }

    }

    const modify_data = [
        {
            name: 'server_port',
            def_obj: def_server_port,
            world_id_list: modify_server_port,
        }, {
            name: 'master_server_port',
            def_obj: def_master_server_port,
            world_id_list: modify_master_server_port,
        }, {
            name: 'authentication_port',
            def_obj: def_authentication_port,
            world_id_list: modify_authentication_port,
        },
    ]

    modify_data.forEach(modify_item => {
        modify_item.world_id_list.forEach((world_id, index) => {
            let new_value = modify_item.def_obj[index] ?? modify_item.def_obj.base + index;
            while (port_value_list.includes(new_value)) {
                new_value++;
            }
            port_value_list.push(new_value);
            input_data[world_id][modify_item.name].placeholder = new_value;
        });
    });

    // name
    input_data[master_world_id].name.placeholder = '[SHDMASTER]';
    const master_world_type = world_id_name[master_world_id].replace(/\d*/g, '');
    const modify_name = [
        {base_name: fix_world_name.forest, world_is_list: sec_forest_id_list},
        {base_name: fix_world_name.cave, world_is_list: sec_cave_id_list},
    ];
    modify_name.forEach(data => {
        data.world_is_list.forEach((world_id, index) => {
            let new_value = data.base_name + (index + ((master_world_type === data.base_name) ? 2 : 1));
            new_value === 'Caves1' && (new_value = 'Caves');
            new_value === 'Master1' && (new_value = 'Master');
            input_data[world_id].name.placeholder = new_value;
        });
    });
}

function create_mod_sider(world_id, world_name, world_type) {
    const sidebar = document.getElementById('mod_sidebar');
    const div = div_();
    div.className = 'world_sidebar_button_div';
    const button = document.createElement('button');
    button.className = 'mod world_sidebar_button show_button';
    button.id = `button_mod_${world_id}`;
    button.innerText = world_name.replace('Master', '森林').replace('Caves', '洞穴');
    button.addEventListener('click', show_event)
    div.appendChild(button);
    
    if (world_type === 'cave') {
        sidebar.appendChild(div);
        return
    }
    const index = [...Object.values(world_id_name)].filter(n => n.startsWith(fix_world_name[world_type])).length;

    index <= sidebar.children.length - 1 ? sidebar.insertBefore(div, sidebar.children[index]) : sidebar.appendChild(div);
}
function create_mod_item(world_id, world_name) {
    const ele_mod = div_();
    ele_mod.className = 'mod_edit focus_item focus_edit hide';
    ele_mod.id = `content_mod_${world_id}`;
    
    const ele_mod_title = div_();
    ele_mod_title.className = 'cluster_title';
    ele_mod.appendChild(ele_mod_title);

    const ele_mod_title_con = document.createElement('h4');
    ele_mod_title_con.className = 'cluster_title_con';
    ele_mod_title_con.innerText = world_name.replace('Master', '森林').replace('Caves', '洞穴') + '模组';
    ele_mod_title.appendChild(ele_mod_title_con);
    
    
    const ele_mod_edit_con = div_();
    ele_mod_edit_con.className = 'mod_edit_con';
    ele_mod.appendChild(ele_mod_edit_con);
    
    const ele_mod_edit_info_part = div_();
    ele_mod_edit_info_part.className = 'mod_edit_info_part';
    ele_mod_edit_info_part.id = `mod_${world_id}_info_part`;
    ele_mod_edit_con.appendChild(ele_mod_edit_info_part);
    
    const ele_mod_button_list = div_();
    ele_mod_button_list.className = 'mod_button_list';
    ele_mod_button_list.id = `mod_${world_id}_button_list`;
    const ele_placeholder = div_();
    ele_placeholder.className = 'mod_card mod_button placeholder';
    const ele_placeholder_text = p_();
    ele_placeholder_text.className = 'mod_button_detail placeholder';
    ele_placeholder_text.innerText = '没有 mod';
    ele_placeholder.appendChild(ele_placeholder_text);
    ele_mod_button_list.appendChild(ele_placeholder);
    ele_mod_edit_info_part.appendChild(ele_mod_button_list);
    
    
    const ele_world_list = document.getElementById('mod_list');
    ele_world_list.appendChild(ele_mod);
}

function create_world_sider(world_id, world_name, world_type) {
    const sidebar = document.getElementById('world_sidebar');
    const div = div_();
    div.className = 'world_sidebar_button_div'
    const button_del = document.createElement('button');
    button_del.className = `world_sidebar_button_menu del${world_id === 'world1' ? ' hidden' : ''}`;
    button_del.id = `button_${world_id}_del`;
    button_del.ondblclick = del_world;
    div.appendChild(button_del);
    const button = document.createElement('button');
    button.className = 'world world_sidebar_button show_button';
    button.id = `button_${world_id}`;
    button.innerText = world_name.replace('Master', '森林').replace('Caves', '洞穴');
    button.addEventListener('click', show_event)
    div.appendChild(button);
    const button_edit = document.createElement('button');
    button_edit.className = `world_sidebar_button_menu edit${world_id === 'world1' ? ' show' : ''}`;
    button_edit.id = `content3_${world_id}`;
    div.appendChild(button_edit);

    if (world_type === 'cave') {
        sidebar.appendChild(div);
        return
    }
    const index = [...Object.values(world_id_name)].filter(n => n.startsWith(fix_world_name[world_type])).length;

    index <= sidebar.children.length ? sidebar.insertBefore(div, sidebar.children[index - 1]) : sidebar.appendChild(div);
}

function is_master_event() {
    if (this.value || this.placeholder === '是') {
        return;
    }
    const is_master_coll = document.getElementsByName('is_master');
    is_master_coll.forEach(input => input.value = '');
    this.value = '是';
    fix_world_info();
}

function create_world_item(world_id, world_name, world_type, isshow = '') {

    const world_obj = dst_world_obj[world_type]


    const ele_world = div_();
    ele_world.className = `world focus_item focus_edit hide${isshow === 'show' ? ' show' : ''}`;
    ele_world.id = `content_${world_id}`;


    const ele_world_title = div_();
    ele_world_title.className = 'cluster_title';
    ele_world.appendChild(ele_world_title);

    const ele_world_title_con = document.createElement('h4');
    ele_world_title_con.className = 'cluster_title_con';
    ele_world_title_con.innerText = world_name.replace('Master', '森林').replace('Caves', '洞穴');
    ele_world_title.appendChild(ele_world_title_con);


    const ele_form = document.createElement('form');
    ele_form.className = 'cluster_item_con no_scroll';
    ele_form.id = `form_${world_id}`;
    ele_form.name = `${world_id}_${world_type}`;
    ele_form.autocomplete = 'off';
    ele_form.action = '';
    ele_world.appendChild(ele_form)

    const ele_form_head = div_();
    ele_form_head.className = 'set_group_head';
    ele_form.appendChild(ele_form_head);

    const form_title = [
        {id: `button_setting_${world_id}`, innerText: '世界选项', state: ' active'},
        {id: `button_gen_${world_id}`, innerText: '世界生成', state: ''},
        {id: `button_server_${world_id}`, innerText: '其他设置', state: ''},
    ]
    for (let title_item of form_title) {
        const ele_form_title = document.createElement('button');
        ele_form_title.className = `${world_id} set_group_title show_button${title_item.state}`;
        ele_form_title.id = title_item.id;
        ele_form_title.type = 'button';
        ele_form_title.onclick = show_event;
        ele_form_title.innerText = title_item.innerText;
        ele_form_head.appendChild(ele_form_title);
    }


    const ele_world_setting = div_();
    ele_world_setting.className = `set_group_${world_id} set_group_con hide show`;
    ele_world_setting.id = `content_setting_${world_id}`;
    ele_form.appendChild(ele_world_setting);

    const ele_world_gen = div_();
    ele_world_gen.className = `set_group_${world_id} set_group_con hide`;
    ele_world_gen.id = `content_gen_${world_id}`;
    ele_form.appendChild(ele_world_gen);

    const ele_world_server = div_();
    ele_world_server.className = `set_group_${world_id} set_group_con hide`;
    ele_world_server.id = `content_server_${world_id}`;
    ele_form.appendChild(ele_world_server);

    const gen = world_obj['WORLDGEN_GROUP'];
    const setting = world_obj['WORLDSETTINGS_GROUP'];
    const gen_group_list = Object.keys(gen).sort((m, n) => gen[m]['order'] - gen[n]['order']);
    const setting_group_list = Object.keys(setting).sort((m, n) => setting[m]['order'] - setting[n]['order']);
    const gen_setting = [
        {obj: gen, list: gen_group_list, ele: ele_world_gen},
        {obj: setting, list: setting_group_list, ele: ele_world_setting},
    ]
    for (let opt_obj of gen_setting) {
        for (let i of opt_obj['list']) {
            // const name = i;
            const desc = opt_obj.obj[i]['desc'];
            const text = opt_obj.obj[i]['text'];
            const items = opt_obj.obj[i]['items'];
            const atlas_obj = opt_obj.obj[i]['atlas'];
            const [atlas, width, height, size] = [atlas_obj.name, atlas_obj.width, atlas_obj.height, atlas_obj["item_size"]];


            const ele_group = div_();
            ele_group.className = 'set_group_item';
            opt_obj.ele.appendChild(ele_group);


            const ele_group_title = div_();
            ele_group_title.className = 'set_group_item_title';
            ele_group_title.innerText = text;
            ele_group.appendChild(ele_group_title);

            const ele_group_con = div_();
            ele_group_con.className = 'set_group_item_con';
            ele_group.appendChild(ele_group_con);

            const item_list = [];
            for (let [j, k] of Object.entries(items)) {
                const item_name = j;  // item key
                const item_text = k['text'];  // 中文名
                const item_image = k['image'];  // item 贴图
                const item_value = k['value'];  // 默认值
                const item_desc = k['desc'] ?? desc;  // item value_list 
                const item_order = k['order']  // 优先级

                const ele_group_item = div_();
                ele_group_item.className = 'set_group_item_con_item';
                item_list.push([item_order, ele_group_item, item_name])


                const ele_item_img = label_();
                ele_item_img.className = 'set_item_img_div';
                ele_item_img.htmlFor = `button_${item_name}_${world_id}`;
                ele_item_img.style.backgroundImage = `url(/misc/${atlas}.webp)`;
                ele_item_img.style.backgroundPosition = `-${Math.round(item_image.x * width / size) * 100}% -${Math.round(item_image.y * height / size) * 100}%`;
                ele_group_item.appendChild(ele_item_img);

                const ele_item = div_();
                ele_item.className = 'set_item_div';
                ele_group_item.appendChild(ele_item);


                const ele_item_label1 = label_();
                ele_item_label1.className = 'world_label world_label_pre emoji_text';
                ele_item_label1.id = `button_${item_name}_${world_id}_pre`;
                ele_item_label1.htmlFor = `button_${item_name}_${world_id}`;
                ele_item.appendChild(ele_item_label1);

                const ele_item_input_div = div_();
                ele_item_input_div.className = 'world_input_div';
                ele_item.appendChild(ele_item_input_div);


                const ele_item_input_title = div_();
                ele_item_input_title.className = 'world_input_title';
                ele_item_input_title.innerText = item_text;
                ele_item_input_title.tabIndex = -1;
                ele_item_input_div.appendChild(ele_item_input_title);
                const ele_item_input = input_();
                ele_item_input.className = 'world_input no_select';
                ele_item_input.id = `button_${item_name}_${world_id}`;
                ele_item_input.name = item_name;
                ele_item_input_title.tabIndex = -1;
                ele_item_input.type = 'text';
                ele_item_input.placeholder = item_desc[item_value];
                const val_index = world_dataset[world_type].list[item_name].indexOf(item_value);
                ele_item_input.dataset.index = '' + val_index;
                ele_item_input.readOnly = true;
                ele_item_input_div.appendChild(ele_item_input);


                const ele_item_label2 = label_();
                ele_item_label2.className = 'world_label world_label_next emoji_text';
                ele_item_label2.id = `button_${item_name}_${world_id}_next`;
                ele_item_label2.htmlFor = `button_${item_name}_${world_id}`;
                ele_item.appendChild(ele_item_label2);

                if (val_index === 0) {
                    ele_item_label1.setAttribute('disabled', '');
                    ele_item_label1.onclick = null;
                } else {
                    ele_item_label1.onclick = function () {
                        change_value('pre', world_type, this);
                    };
                }
                if (val_index === world_dataset[world_type].list[item_name].length - 1) {
                    ele_item_label2.setAttribute('disabled', '');
                    ele_item_label2.onclick = null;
                } else {
                    ele_item_label2.onclick = function () {
                        change_value('next', world_type, this);
                    };
                }
            }

            item_list.sort((m, n) => {
                if (!isFinite(m[0]) && !isFinite(n[0])) {
                    return m[2] > n[2] ? 1 : -1;
                } else if (isFinite(m[0]) && isFinite(n[0])) {
                    return m[0] > n[0] ? 1 : -1;
                } else {
                    return isFinite(m[0]) ? -1 : 1;
                }
            })
            item_list.forEach(n => ele_group_con.appendChild(n[1]));
            for (let i = 0; i < ele_group_con.childNodes.length % 3; i++) {
                const ele_group_item = div_();
                ele_group_item.className = 'set_group_item_con_item';
                ele_group_con.appendChild(ele_group_item);
            }
        }
    }

    // server
    const ele_server_con = div_();
    ele_server_con.className = 'cluster_item_con edit_items';
    ele_world_server.appendChild(ele_server_con);
    const ele_server_con_list = div_();
    ele_server_con_list.className = 'cluster_item_list';
    ele_server_con.appendChild(ele_server_con_list);


    const server_date = [
        {
            label_for: `button_server_port_${world_id}`,
            label_text: '服务器端口',
            className: 'cluster_item_div_input show_button',
            id: `button_server_port_${world_id}`,
            name: 'server_port',
            pattern: '0*(1((0(2[5-9]|[3-9][0-9]))|([1-9][0-9]{2}))|[2-9][0-9]{3}|[1-6][0-9]{4})',
            placeholder: {world1: 10999, world2: 10998}[world_id] || +world_id.replace('world', '') + 10997,
            type: 'tel',
            onblur: fix_world_info,
        },
        {
            label_for: `button_is_master_${world_id}`,
            label_text: '主世界',
            className: 'cluster_item_div_input show_pl no_select show_button',
            id: `button_is_master_${world_id}`,
            name: 'is_master',
            placeholder: world_id.replace('world', '') === '1' ? '是' : '否',
            readOnly: true,
            type: 'text',
            ondblclick: is_master_event,
        },
        {
            label_for: `button_name_${world_id}`,
            label_text: '世界名',
            className: 'cluster_item_div_input show_pl no_select show_button',
            id: `button_name_${world_id}`,
            name: 'name',
            placeholder: world_name,
            readOnly: true,
            type: 'text',
        },
        {
            label_for: `button_id_${world_id}`,
            label_text: '世界 ID',
            className: 'cluster_item_div_input show_pl no_select show_button',
            id: `button_id_${world_id}`,
            name: 'id',
            placeholder: world_id.replace('world', ''),
            readOnly: true,
            type: 'tel',
        },
        {
            label_for: `button_encode_user_path_${world_id}`,
            label_text: '路径兼容',
            className: 'cluster_item_div_input show_pl no_select show_button',
            id: `button_encode_user_path_${world_id}`,
            name: 'encode_user_path',
            placeholder: '开启',
            readOnly: true,
            type: 'text',
        },
        {
            label_for: `button_authentication_port_${world_id}`,
            label_text: '认证端口',
            className: 'cluster_item_div_input show_button',
            id: `button_authentication_port_${world_id}`,
            name: 'authentication_port',
            pattern: '0*(1((0(2[5-9]|[3-9][0-9]))|([1-9][0-9]{2}))|[2-9][0-9]{3}|[1-6][0-9]{4})',
            placeholder: +world_id.replace('world', '') + 8765,
            type: 'tel',
            onblur: fix_world_info,
        },
        {
            label_for: `button_master_server_port_${world_id}`,
            label_text: '世界端口',
            className: 'cluster_item_div_input show_button',
            id: `button_master_server_port_${world_id}`,
            name: 'master_server_port',
            pattern: '0*(1((0(2[5-9]|[3-9][0-9]))|([1-9][0-9]{2}))|[2-9][0-9]{3}|[1-6][0-9]{4})',
            placeholder: +world_id.replace('world', '') + 27015,
            type: 'tel',
            onblur: fix_world_info,
        },
    ]
    for (let attr_data of server_date) {
        const ele_server_item = div_();
        ele_server_item.className = 'cluster_edit_item';
        ele_server_con_list.appendChild(ele_server_item);
        const ele_item_label = label_();
        ele_item_label.className = 'cluster_item_label';
        ele_item_label.htmlFor = attr_data.label_for;
        ele_item_label.innerText = attr_data.label_text;
        ele_server_item.appendChild(ele_item_label)
        const ele_item_div = div_();
        ele_item_div.className = 'cluster_item_div';
        ele_server_item.appendChild(ele_item_div);
        const ele_item_input = input_();
        ele_item_input.addEventListener('keydown', (KeyboardEvent)=>{
            KeyboardEvent.key === "Enter" && ele_item_input.blur();
        });
        [...Object.entries(attr_data)].forEach(attr => {
            if (!attr[0].startsWith('label')) {
                ele_item_input[attr[0]] = attr[1];
            }
        });
        ele_item_div.appendChild(ele_item_input);
    }


    for_show_button(ele_server_con_list.getElementsByClassName('show_button'));

    // server

    const ele_world_list = document.getElementById('world_list')
    ele_world_list.appendChild(ele_world)

}

function for_show_button(show_buttons) {
    for (let show_button of show_buttons) {
        // const type = ['INPUT', 'TEXTAREA'].includes(show_button.tagName) ? 'focus' : 'click';
        const type = ['INPUT', 'TEXTAREA'].includes(show_button.tagName) ? 'mouseover' : 'click';
        show_button.addEventListener(type, show_event);
        ['INPUT', 'TEXTAREA'].includes(show_button.tagName) && show_button.addEventListener('input', show_event);
       
    }
}

function show_event() {
    
    let class_button;
    for (let j of this.classList.values()) {
        // if (j === 'active') {
        //     return;
        // }
        if (!class_button) {
            class_button = j;
        }
    }
    // 清除 active，再添加 active    取消 active 方法是：寻找 .classlist[0].active
    const buttons_act = document.getElementsByClassName(class_button + ' active');
    for (let button_unact of [...buttons_act]) {
        button_unact.classList.remove('active');
    }
    this.classList.add('active');

    // 清除 show，再添加 show     取消 show 方法是：寻找 .classlist[0].show
    const content_list = [this.id.replace('button', 'content'), this.id.replace('button', 'content2').replace(/world\d+/, 'world'), this.id.replace('button', 'content3')];
    for (let id of content_list) {
        const content = document.getElementById(id);
        if (content) {
            const class_content = [...content.classList.values()][0];
            const contents_act = document.getElementsByClassName(class_content + " show");
            for (let content_unshow of [...contents_act]) {
                content_unshow.classList.remove('show');
            }
            content.classList.add('show');
        }
    }
}

function emoji_bar() {
    if (!([...document.getElementById('emoji_bar').classList].find((n) => n === 'active'))) {
        document.getElementById('emoji_bar').classList.add('active');
        this.classList.add('active')
    } else {
        document.getElementById('emoji_bar').classList.remove('active');
        this.classList.remove('active')
    }
}

function change_value(purpose, verify, label) {
    let dataset;
    if (verify === 'cluster') {
        dataset = cluster_dataset;
    } else if (['forest', 'cave'].includes(verify)) {
        dataset = world_dataset[verify];
    } else {
        console.log('change_value: value of the verify is wrong !');
        return;
    }
    
    const [key_val, key_list, val_def] = [dataset.code, dataset.list, dataset.default];
    
    const input = document.getElementById(label.htmlFor);
    const name = input.name;
    let old_index = +input.dataset.index;
    const [item_dataset, value_list, default_val] = [key_val[name], key_list[name], val_def[name]];
    
    if (!value_list) {
        console.log(`channge_value: ${input.id} don\'t have a value list !`);
        return;
    }
    if (!(0 <= old_index && old_index <= value_list.length - 1)) {
        // 应该什么都不需要做吧
        console.log('channge_value: index超出正常范围，将从 0 开始计算', input);
        old_index = 0;
    }

    // 获取新的 index
    let new_index;
    if (purpose === 'pre') {
        new_index = (old_index === 0) ? old_index : old_index - 1;
    } else if (purpose === 'next') {
        new_index = (old_index === value_list.length - 1) ? old_index : old_index + 1;
    } else {
        console.log('change_value: purpose is wrong !');
        return;
    }

    // 修正 label 的状态
    const label_pre = document.getElementById(input.id + '_pre');
    const label_next = document.getElementById(input.id + '_next');
    if (old_index === 0) {
        label_pre.removeAttribute('disabled');
        label_pre.onclick = function () {
                change_value('pre', verify, this);
            };
    }
    if (old_index === value_list.length - 1) {
        label_next.removeAttribute('disabled');
        label_next.onclick = function () {
                change_value('next', verify, this);
            };
    }
    if (new_index === 0) {
        label_pre.setAttribute('disabled', '');
        label_pre.onclick = null;
    }
    if (new_index === value_list.length - 1) {
        label_next.setAttribute('disabled', '');
        label_next.onclick = null;
    }

    // 赋新值
    input.dataset.index = new_index;
    if (new_index === key_list[name].indexOf(default_val)) {
        input.style.background = 'none';
        if (input.placeholder === '') {
            input.value = item_dataset[default_val];
        } else {
            input.value = '';
        }
    } else {
        const new_value = item_dataset[value_list[new_index]];
        input.style.backgroundColor = 'rgba(127, 127, 127, 20%)';
        input.value = new_value;
    }
}

// textarea 自动调高
for (let area of document.getElementsByTagName('textarea')) {
    area.addEventListener('input', function () {
            this.style.height = "1px";
            this.style.height = (this.scrollHeight) + "px";
        }
    );
}


// 平滑滚动
window.scrollTo({top: 0, behavior: 'smooth'});

// 筛选出符合规则的 ID
function select_userid(eleid, base_class) {
    function select_userid_single(eleid, data, type, classname, pattern, column_num) {
        // 不存在目标父节点就退出
        const ele_old_id_list = document.getElementById(eleid.replace('raw_button', type));
        if (!ele_old_id_list) {
            return;
        }
    
        // 不存在有效数据就退出
        const id_list = data.match(pattern);
        if (!id_list) {
            return;
        }
    
        // 获取已经添加的 ID 列表
        const old_id_list = [...ele_old_id_list.childNodes.values()].map((ele) => ele.value).filter((value) => value);
    
        // 去重，保留未被添加过的 ID
        const new_id_list = [...new Set(old_id_list.concat(id_list))].slice(old_id_list.length);
    
        // 创建文档片段并添加目标元素
        const list_frag = document.createDocumentFragment();
        for (let id_index = 0; id_index < new_id_list.length; id_index++) {
            const ele_id = input_();
            const user_id = new_id_list[id_index];
            ele_id.className = classname;
            ele_id.name = id_index.toString();
            ele_id.value = user_id;
            ele_id.column = column_num;
            ele_id.tabIndex = -1;
            ele_id.ondblclick = remove_update_idnum;
            ele_id.readOnly = true;
            list_frag.appendChild(ele_id);
        }
    
        // 文档片段末尾追加占位元素用于对齐
        const classname_hide = classname + ' hide_item';
        for (let i = 0; i < column_num; i++) {
            const new_input = div_();
            new_input.className = classname_hide;
            list_frag.appendChild(new_input);
        }
    
        // 清理原有的占位元素
        const hiden = ele_old_id_list.getElementsByClassName('hide_item');
        for (let i = hiden.length - 1; i >= 0; i--) {
            hiden[i].remove();
        }
    
        // 文档片段插入页面
        ele_old_id_list.appendChild(list_frag);
    
        // 更新标题子元素数量
        update_idnum(ele_old_id_list, column_num + 1);
    }
    
    function remove_update_idnum() {
        const parent = this.parentElement;
        this.remove();
        update_idnum(parent, this.column + 1);
    }
    
    const input = document.getElementById(eleid.replace('_button', ''));
    const data = input.value;
    input.value = '';
    if (!data) {
        return;
    }

    const type_list = {
        kid: {
            classname: `${base_class} no_select kid`,
            pattern: /KU_[\w-]{8}/gm,
            column_num: 3
        },
        sid: {
            classname: `${base_class} no_select sid`,
            pattern: /76561[0-9]{12}/gm,
            column_num: 4
        }
    }

    for (let type in type_list) {
        select_userid_single(eleid, data, type, ...Object.values(type_list[type]));
    }
}

// 更新已添加的 id 的数量
function update_idnum(ele, num) {
    const new_count = (ele.childElementCount - num).toString();
    const title = ele.getElementsByClassName('title')[0];
    title.innerText = title.innerText.replace(/(?<h>klei id: 共 |steam id: 共 )[\d\D]+(?<f> 个)/, '$<h>' + new_count + '$<f>');
}

// 清理添加的 id
function clean_bro(ele) {
    const parent = ele.parentElement;
    const id_list = parent.getElementsByClassName('cluster_black_item');
    for (let i = id_list.length - 1; i >= 0; i--) {
        id_list[i].remove();
    }
    parent.scrollIntoView();
    update_idnum(parent, 1);
}

function close_parent(ele=null) {
    const par = (this === window ? ele : this).parentElement;
    const close_class = 'close';
    if (par.classList.contains(close_class)) {
        par.classList.remove(close_class);
    } else {    
        par.classList.add(close_class);
    }
}

// 选择表单
function select_form() {
    if (!check_form()) {
        return;
    }
    const world_id_dir = {};
    const result = {mod:{}};
    const form_list = [...document.getElementsByTagName('form')];
    for (let form of form_list) {
        const data = new FormData(form);
        let data_json = {};
        let form_name = form.getAttribute('name');
        if (form_name === 'cluster') {
            const tmp_cluster = {...cluster_dataset.default};
            data.forEach((value, key) => {
                if (value) {
                    if (cluster_dataset.code.hasOwnProperty(key)) {
                        for (let [key_, value_] of Object.entries(cluster_dataset.code[key])) {
                            if (value_ === value) {
                                value = key_;
                            }
                        }
                    }
                    tmp_cluster[key] = value;
                }
            });
            const cluster_order = ['[GAMEPLAY]', 'game_mode', 'max_players', 'pause_when_empty', 'pvp', 'vote_enabled', '', '[NETWORK]', 'cluster_name', 'cluster_description', 'cluster_intention', 'cluster_password', 'cluster_language', 'autosaver_enabled', 'connection_timeout', 'idle_timeout', 'lan_only_cluster', 'offline_cluster', 'override_dns', 'tick_rate', 'whitelist_slots', '', '[MISC]', 'autocompiler_enabled', 'console_enabled', 'max_snapshots', '', '[STEAM]', 'steam_group_admins', 'steam_group_id', 'steam_group_only', '', '[SHARD]', 'shard_enabled', 'bind_ip', 'master_ip', 'master_port', 'cluster_key',];
            let new_value = '';
            for (let i of cluster_order) {
                new_value += `${i}${tmp_cluster.hasOwnProperty(i) ? (' = ' + tmp_cluster[i]) : ''}\n`;
            }
            data_json = new_value;
        } else if (['token', 'admin', 'black', 'white'].includes(form_name)) {
            data_json = [...data.values()].filter(n => n).join('\n');
        } else if (form_name.startsWith('world')) {
            // form_name world\d+_[forest/cave]
            const [world_data, server_data] = [{}, {}];
            let world_code, suf_name, world_type;
            if (form_name.endsWith('forest')) {
                world_type = 'forest';
                world_code = world_dataset.forest.code;
                suf_name = form_name.replace('_forest', '');
            } else if (form_name.endsWith('cave')) {
                world_type = 'cave';
                world_code = world_dataset.cave.code;
                suf_name = form_name.replace('_cave', '');
            }
            
            data.forEach((value, key) => {
                if (value) {
                    if (world_code.hasOwnProperty(key)) {
                        for (let [key_, value_] of Object.entries(world_code[key])) {
                            if (value === value_) {
                                value = key_;
                            }
                        }
                    }
                    world_data[key] = value;
                }
            });
            const world_preset = {forest: 'SURVIVAL_TOGETHER', cave: 'DST_CAVE'}[world_type];
            const world_item_str = [...Object.entries(world_data)].map(n => `${n[0]} = "${n[1]}"`).join(',\n\t\t');
            data_json.world = `KLEI     1 return {\n\toverride_enabled = true,\n\tsettings_preset = "${world_preset}",\n\tworldgen_preset = "${world_preset}",\n\toverrides = {${world_item_str.length ? '\n\t\t' + world_item_str + ',\n\t' : ''}},\n}`;
            
            const server_list = ['id', 'name', 'is_master', 'server_port', 'encode_user_path', 'master_server_port', 'authentication_port'];
            const server_code = {is_master: {是: 'true', 否: 'false'}, encode_user_path: {开启: 'true', 关闭: 'false'}};
            server_list.forEach(key => {
                if (!world_data.hasOwnProperty(key)) {
                    server_data[key] = document.getElementById(`button_${key}_${suf_name}`).placeholder;
                } else {
                    server_data[key] = world_data[key];
                    delete world_data[key];
                }
                if (server_code.hasOwnProperty(key)) {
                    server_data[key] = server_code[key][server_data[key]];
                }
            });
            const server_order = ['[NETWORK]', 'server_port', '', '[SHARD]', 'is_master', 'name', 'id', '', '[ACCOUNT]', 'encode_user_path', '', '[STEAM]', 'authentication_port', 'master_server_port']
            let server_str = '';
            for (let i of server_order) {
                server_str += `${i}${server_data.hasOwnProperty(i) ? (' = ' + server_data[i]) : ''}\n`;
            }
            data_json.server = server_str;
            
            const world_id = form_name.replace('_forest', '').replace('_cave', '');
            form_name = (server_data.name !== '[SHDMASTER]') ? server_data.name : form_name.endsWith('forest') ? 'Master' : 'Caves';
            
            world_id_dir[world_id] = form_name;
        } else if (form_name.startsWith('mod')) {
            // input 的 value 都是字符串，不好还原原本值的类型，自己筛选用 index 获取
            const mod_data = {};
            const [world_id, modid] = /mod_([^_]+)_(\d+)/.exec(form_name).slice(1);
            const modinfo = modinfo_dataset[modid];
            const inputs = form.getElementsByTagName('input');
            [...inputs].forEach((input) => {
                let [name, index] = [input.name, +input.dataset.index];
                const item_data = modinfo[name];
                mod_data[name] = item_data.dataset[index].data ?? item_data.dataset[item_data.default_index].data;
            });
            result.mod[world_id] ??= {};
            result.mod[world_id][modid] = mod_data;
            continue;
        }
        result[form_name] = data_json;
    }
    // return {["workshop-1216718131"]={ configuration_options={ clean=true, lang=true, stack=false }, enabled=true },}
    function data_table(data) {
        // num, str, boolean, array, object, null
        if (['number', 'string', 'boolean'].includes(typeof data) || data === null) {
            return JSON.stringify(data);
        }
        if (Array.isArray(data)) {
            return `{${data.map(n=>data_table(n)).join(',')}}`;
        }
        if (Object.prototype.toString.call(data) === '[object Object]') {
            return `{${Object.entries(data).map(n=>`[${data_table(n[0])}]=${data_table(n[1])}`).join(',')}}`;
        }
        // ubdefined, symbol, function, ...
        console.log('??? 你传来了什么数据', data);
    }
    function modobj_text(modobj) {
        let text = '';
        Object.entries(modobj).forEach(moddata => {
            const [modid, mod_item] = moddata;
            text = text + `["workshop-${modid}"]={ configuration_options=${data_table(mod_item)}, enabled=true },\n`;
        })
        return text ? '\n' + text : text;
    }
    const mod_data = result.mod;
    const others = {};
    const common = mod_data['common'] ?? {};
    const text_common = `return {${modobj_text(common)}}`;

    for (let [world_id, mod_items] of Object.entries(mod_data)) {
        if (world_id !== 'common') {
            others[world_id_dir[world_id]] = `return {${modobj_text({...common, ...mod_items})}}`;
        }
    }
    
    Object.keys(result).forEach(n=>{
        if (!/Master|Caves/.test(n)) {
            return;
        }
        result[n].mod = others[n] || text_common;
    })
    delete result.mod;
    if(!result.token) {
        result.token = 'pds-g^KU_iNDUz9EQ^Fs+rcQpM+INprasSYAlh9obhwrnAwkNMdFYbEcOJRuE=';
    }

    return result;
}

function check_form() {
    const form_list = [...document.getElementsByTagName('form')];
    for (let form of form_list) {
        if (!form.checkValidity()) {
            // TODO 提醒
            alert('表单验证未通过');
            return false;
        }
    }
    return true;
}

async function lets_go() {
    const url = 'tools/cluster';
    const data = select_form();
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            charset: 'utf-8'
        }, 
        body: JSON.stringify(data),
    }).catch(err=>console.log(err));
    if (!response.ok) {
        throw new Error('world_json wrong, network code: ' + response.statusText);
    }
    const link_suf = await response.text();
    const link = `${window.location.href}clusters/${link_suf}/`
    const file_zip = link + 'MyDediServer.zip';
    const file_tar = link + 'MyDediServer.tar';

    const done = document.getElementById('content_done');
    const link_zip = a_();
    link_zip.id = 'file_zip';
    link_zip.className = 'done_link normal_link';
    link_zip.href = file_zip;
    link_zip.title = '下载 zip 格式文件';
    link_zip.target = '_blank';
    link_zip.innerText = '下载存档 zip';
    link_zip.download = "MyDediServer.zip";

    const link_tar = a_();
    link_tar.id = 'file_tar';
    link_tar.className = 'done_link normal_link';
    link_tar.href = file_tar;
    link_tar.title = '下载 tar 格式文件';
    link_tar.target = '_blank';
    link_tar.innerText = '下载存档 tar';
    link_tar.download = 'MyDediServer.tar';

    for (let ele_id of ['file_zip', 'file_tar']) {
        const ele_old = document.getElementById(ele_id);
        if (ele_old) {
            ele_old.remove();
        }
    }

    done.appendChild(link_zip);
    done.appendChild(link_tar);

    return [file_zip, file_tar];
}


async function get_world_json() {
    const url = 'misc/dst_world_setting.json';
    const world_group_file = await fetch(url, {method: 'GET', mode: 'cors',}).catch(async ()=>{return await fetch(url, {method: 'GET', mode: 'cors',});});
    if (world_group_file.ok) {
        return await world_group_file.json();
    } else {
        throw new Error('world_json wrong, network code: ' + world_group_file.statusText);
    }
}

function hide_ele(ele) {
    if (ele && !ele.classList.contains('hide')) {
        ele.classList.add('hide');
    }
}
function show_ele(ele) {
    if (ele) {
        ele.classList.remove('hide');
    }
}

function search_event() {
    
    function search_mod(text) {
        // let url = window.location.href + '/tools/searchmod';
        let url = 'tools/searchmod';

        url = add_url_param(url, 'text', text);

        return fetch(url, {method: 'GET', mode: 'cors',});
    }

    (async function get_auth_name(base_link=null) {
        if (base_link === null) {
            return;
        }
        const link = `${base_link}?xml=1`;
        const response = await fetch(link, {method: 'GET', mode: 'cors',});
        if (!response.ok) {
            return '我不知道';
        } else {
            const auth_info = await response.text();
            const auth_name_ = auth_info.match(/<steamID><!\[CDATA\[(.*?)]]><\/steamID>/);
            return auth_name_ ? auth_name_[1] : '无名之人';
        }
    })();
    
    const search_text = document.getElementById('mod_search_add').value;
    if (search_text === '') {
        return;
    }
    const [task_name, start_time] = ['search_event', Date.now()]
    if (!can_i_press(task_name, start_time)) {
        return;
    }
    
    const mod_result_list = document.getElementById('mod_result_list');
    const mod_card_list = document.getElementById('content_mod_select');
    const mod_search_start = document.getElementById('mod_search_start');
    const mod_card_searching = document.getElementById('mod_searching');
    const mod_search_failed = document.getElementById('mod_search_failed');
    const mod_search_none = document.getElementById('mod_search_none');

    hide_ele(mod_search_start);
    hide_ele(mod_search_failed);
    hide_ele(mod_search_none)
    if (mod_card_list) {
        hide_ele(mod_card_list);
        mod_card_list.remove();
    }
    show_ele(mod_card_searching);
    search_mod(search_text)
        .then(result => {
            result.json().then(mod_result => {
                if (!mod_result.length) {
                    hide_ele(mod_card_searching);
                    show_ele(mod_search_none);
                    return;
                }
                const new_mod_list = div_();
                new_mod_list.className = 'desc_for_mod cluster_desc_item mod_desc_item';
                new_mod_list.id = 'content_mod_select';
    
                for (let {img, child, ...modinfo} of mod_result) {
    
                    const mod_card = div_();
                    mod_card.className = 'mod_card';
                    const mod_img = div_();
                    mod_img.className = 'mod_card_img';
                    const suf_url = '?imw=128&imh=128&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true';
                    const img_url = img ? img + suf_url : '/misc/idk.png';
                    mod_img.style.backgroundImage = `url(${img_url})`;
                    const mod_img_add = div_();
                    mod_img_add.className = 'mod_card_img_add';
                    mod_img_add.onclick = () => add_mod_to_world(modinfo['id']);
                    mod_img_add.child = child;
                    mod_img_add.innerHTML = '添加<br>模组';
                    mod_img.appendChild(mod_img_add);
                    mod_card.appendChild(mod_img);
                    const mod_info = div_();
                    mod_info.className = 'mod_card_info';
                    mod_card.appendChild(mod_info);
                    
                    for (let item of ['name', 'id', 'auth', 'vote', 'sub', 'time']) {
                        const card_item = div_();
                        card_item.className = 'mod_card_info_item';
                        
                        const value = modinfo[item]
                        
                        if (item === 'name') {
                            card_item.innerText = value;
                            card_item.title = value;
                        } else if (item === 'id') {
                            card_item.title = 'mod id 点击查看 steam 页面';
                            const link = document.createElement('a');
                            link.className = 'normal_link';
                            link.target = '_blank';
                            link.innerText = value;
                            link.href = `https://steamcommunity.com/sharedfiles/filedetails/?id=${value}`;
                            card_item.appendChild(link);
                        } else if (item === 'vote') {
                            const vote_star = value['star']
                            const vote_num = value['num'];
                            card_item.innerText = '★'.repeat(vote_star) + '☆'.repeat(5 - vote_star);
                            card_item.title = vote_star ? `${vote_num}个评分` : '评价数不足';
                        } else if (item === 'auth') {
                            card_item.title = '作者 点击查看个人主页';
                            const auth_url = `https://steamcommunity.com/profiles/${value}/`
                            const link = document.createElement('a');
                            link.className = 'normal_link';
                            link.target = '_blank';
                            link.href = auth_url;
                            link.innerText = '作者主页';
                            // get_auth_name(auth_url)
                            //     .then(auth => {
                            //         link.innerText = auth;
                            //     })
                            //     .catch(() => {
                            //         link.innerText = '我不知道';
                            //     });
                            card_item.appendChild(link);

                        } else if (item === 'sub') {
                            card_item.innerText = '⚐' + value;
                            card_item.title = '订阅数量';
                        } else if (item === 'time') {
                            card_item.innerText = new Date(value * 1000).toLocaleString('zh-CN');
                            card_item.title = '最后更新时间';
                        }
                        mod_info.appendChild(card_item);
                    }
                    new_mod_list.appendChild(mod_card);
                }
                
                if (new_mod_list.children.length >= 25) {
                    const see_nothing = div_();
                    see_nothing.className = 'mod_card';
                    see_nothing.innerText = '还看吗？不给看';
                    new_mod_list.appendChild(see_nothing);
                }
                
                hide_ele(mod_card_searching);
                if (lastest_self[task_name] === start_time) {
                    mod_result_list.appendChild(new_mod_list);
                }
            })
        })
        .catch(err => {
            console.log(err)
            hide_ele(mod_card_searching);
            show_ele(mod_search_failed);
        })
        .then(() => {
            run_tried(task_name);
        });
}

async function add_mod_to_world(modid, nocheck=false) {
    modid = '' + modid;
    if (!/\d{9,10}/.test(modid)) {
        tip('不是id不要乱加');
        return;
    }
    const ele_active_mod_page = document.getElementsByClassName('mod_edit show')[0];
    const pre_id = ele_active_mod_page.id.replace('content_', '');
    const sign_id = `${pre_id}_${modid}`;
    const ele_info_part = document.getElementById(`${pre_id}_info_part`);
    const ele_mod_list = document.getElementById(`${pre_id}_button_list`);
    const ele_mod_list_placeholder = ele_mod_list.getElementsByClassName('placeholder')[0];
    
    if (document.getElementById(`button_${sign_id}`)) {
        alert('该 mod 已经添加过了');
        return;
    }
    
    if (!nocheck && !can_i_press(`add_mod_to_world_${modid}`, Date.now())) {
        return;
    }
    
    let modinfo;
    if (mod_info_saved[modid]) {
        modinfo = mod_info_saved[modid];
    } else {
        const url = `tools/mod/${modid}`;
        const json = await fetch(url, {method: 'GET', mode: 'cors',}).then(response => response.json()).catch(err=>{console.log(err);alert('连接服务器失败')});
        
        const status = json.status;

        if (status !== 1 && status !== 2) {
            // TODO 获取 modinfo 失败
            alert('获取 modinfo 失败');
            run_tried(`add_mod_to_world_${modid}`);
            return;
        }
        // if (status === 2) {
        //     modinfo 为空
        // }
        modinfo = json["modinfo"];

        mod_info_saved[modid] = modinfo;
    }
    
    if (modinfo.client_only_mod) {
        // TODO 是客户端 mod
        alert('不是服务器 mod');
        run_tried(`add_mod_to_world_${modid}`);
        return;
    }
    
    const info_list = {
        name: '名称',
        version: '版本',
        author: '作者',
    }
    const forum = 'forumthread';
    const modtype = {
        client_only_mod: '仅客户端开启',
        server_only_mod: '仅服务器开启',
        all_clients_require_mod: '客户端与服务器都需开启',
    }
    const compatible = {
        dst_compatible: '饥荒：联机版',
        forge_compatible: '熔炉',
        gorge_compatible: '暴食',
    }
    const desc = 'description';
    const dependency = 'mod_dependencies';
    const configuration = 'configuration_options';

    
    // 显示mod名和id的卡片
    const ele_mod_button = div_();
    ele_mod_button.className = `${pre_id} mod_card mod_button show_button`;
    ele_mod_button.id = `button_${sign_id}`;
    ele_mod_button.onclick = show_event;
    const ele_mod_button_name = p_();
    ele_mod_button_name.className = 'mod_button_detail';
    ele_mod_button_name.title = modinfo.name || '无名之名';
    ele_mod_button_name.innerText = modinfo.name || '无名之名';
    const ele_mod_button_modid = p_();
    ele_mod_button_modid.className = 'mod_button_detail';
    ele_mod_button_modid.innerText = modid;
    ele_mod_button.appendChild(ele_mod_button_name);
    ele_mod_button.appendChild(ele_mod_button_modid);
    
    // 显示modinfo
    const ele_mod_info_con = div_();
    ele_mod_info_con.className = `${pre_id} mod_info_list hide`;
    ele_mod_info_con.id = `content_${sign_id}`;
    
    const ele_mod_info_del = div_();
    ele_mod_info_del.className = 'mod_description_close mod_info_del';
    ele_mod_info_del.onclick = ()=>{
        ele_mod_button.remove();
        ele_mod_info_con.remove();
        if (ele_mod_list.getElementsByClassName('show_button').length === 0) {
            show_ele(ele_mod_list_placeholder);
        }
    }
    ele_mod_info_del.innerHTML = '<div class="emoji_text">󰀀</div>';
    ele_mod_info_con.appendChild(ele_mod_info_del);
    
    
    const ele_mod_description_close = div_();
    ele_mod_description_close.className = 'mod_description_close';
    ele_mod_description_close.onclick = close_parent;
    ele_mod_description_close.innerHTML = '<div class="emoji_text">󰀅</div>';
    ele_mod_info_con.appendChild(ele_mod_description_close);

    function create_new_row(column1, column2, type='innerText') {
        const item_tr = tr_();
        const item_key = td_();
        item_key[type] = column1;
        const item_value = td_();
        item_value[type] = column2;
        item_tr.appendChild(item_key);
        item_tr.appendChild(item_value);
        return item_tr;
    }
    const ele_mod_description = div_();
    ele_mod_description.className = 'mod_description';
    ele_mod_info_con.appendChild(ele_mod_description);
    const ele_mod_description_item = table_();
    ele_mod_description_item.className = 'mod_description_item';
    ele_mod_description.appendChild(ele_mod_description_item);
    // 'name', 'version', 'author', 'server_filter_tags'
    for (let [item_name, item_value] of Object.entries(info_list)) {
        const item_tr = create_new_row(item_value, modinfo[item_name] || '我不知道');
        ele_mod_description_item.appendChild(item_tr);
    }
    // forumthread
    const reg_link = /\/?(files|forums|profile)?\/?(file|topic)\/\d+-/;
    if (modinfo.hasOwnProperty(forum) && reg_link.test(modinfo[forum])) {
        const klei_link_pre = 'https://forums.kleientertainment.com';
        let forumurl = modinfo[forum];
        if (forumurl.startsWith('http')) {
            // 原链接，什么也不做
        } else if (forumurl.startsWith('/files') || forumurl.startsWith('/profile')) {
            forumurl = klei_link_pre + forumurl;
        } else if (forumurl.startsWith('files') || forumurl.startsWith('profile')) {
            forumurl = klei_link_pre + '/' + forumurl;
        } else if (forumurl.startsWith('/file')) {
            forumurl = klei_link_pre + '/files' + forumurl;
        } else if (forumurl.startsWith('file')) {
            forumurl = klei_link_pre + '/files/' + forumurl;
        } else if (forumurl.startsWith('/forums')) {
               forumurl = klei_link_pre + forumurl;
        } else if (forumurl.startsWith('forums')) {
            forumurl = klei_link_pre + '/' + forumurl;
        } else if (forumurl.startsWith('/topic')) {
            forumurl = klei_link_pre + '/forums' + forumurl;
        } else if (forumurl.startsWith('topic')) {
            forumurl = klei_link_pre + '/forums/' + forumurl;
        } else {
            console.log('这什么鬼链接', forumurl);
        }
        const ele_forum = a_();
        ele_forum.className = 'normal_link';
        ele_forum.innerText = '点击前往';
        ele_forum.href = forumurl;
        ele_forum.target = '_blank';
        ele_forum.title = '点击访问预留的 mod 主页';
        const item_tr = create_new_row('主页', ele_forum.outerHTML, 'innerHTML');
        ele_mod_description_item.appendChild(item_tr);
    }
    // 'client_only_mod', 'server_only_mod', 'all_clients_require_mod'
    let client_server;
    if (modinfo.all_clients_require_mod) {
        client_server = modtype.all_clients_require_mod;
    } else if (modinfo.server_only_mod) {
        client_server = modtype.server_only_mod;
    } else if (modinfo.client_only_mod) {
        client_server = modtype.client_only_mod;
    } else {
        client_server = modtype.all_clients_require_mod;
    }
    const ele_client_server = create_new_row('类别', client_server);
    ele_mod_description_item.appendChild(ele_client_server)
    
    // 'dst_compatible', 'forge_compatible', 'gorge_compatible'
    let mod_compatible = [];
    if (modinfo.dst_compatible) {
        mod_compatible.push(compatible.dst_compatible);
    }
    if (modinfo.forge_compatible) {
        mod_compatible.push(compatible.forge_compatible);
    }
    if (modinfo.gorge_compatible) {
        mod_compatible.push(compatible.gorge_compatible);
    }
    mod_compatible = mod_compatible.join('、') || '我不知道';
    const ele_compatiable = create_new_row('兼容性', mod_compatible);
    ele_mod_description_item.appendChild(ele_compatiable);
    // mod_dependencies
    const mod_dependency = modinfo[dependency]?.map(n=>n["workshop"]?.replace("workshop-", "")).filter(n=>n);
    if (mod_dependency && mod_dependency.length !== 0) {
        const ele_mod_dependency = create_new_row('依赖 mod', mod_dependency.join('、'));
        ele_mod_description_item.appendChild(ele_mod_dependency);
        setTimeout(()=>{
            // TODO 处理依赖 mod
            alert(`${modinfo.name || modid} 需要以下 mod 才可正常使用，将自动添加\n` + mod_dependency.join('、'));
            for (let dep_modid of mod_dependency) {
                if (!document.getElementById(`button_${pre_id}_${dep_modid}`)) {
                    add_mod_to_world(dep_modid, 'no check');
                }
            }
        }, 100)
    }
    const ele_mod_link = a_();
    ele_mod_link.className = 'normal_link';
    ele_mod_link.innerText = modid;
    ele_mod_link.href = `https://steamcommunity.com/sharedfiles/filedetails/?id=${modid}`;
    ele_mod_link.target = '_blank';
    ele_mod_link.title = '查看 steam 创意工坊页面';
    const ele_mod_link_ = create_new_row('创意工坊', ele_mod_link.outerHTML, 'innerHTML');
    ele_mod_description_item.appendChild(ele_mod_link_);
    
    // description
    if (modinfo[desc]) {
        const ele_mod_desc = div_();
        ele_mod_desc.className = 'mod_desc';
        ele_mod_desc.innerText = modinfo[desc];
        ele_mod_description.appendChild(ele_mod_desc);
    }
    
    // configuration_options
    const mod_configs_list = [];
    if (Array.isArray(modinfo[configuration])) {
        const is_nothing = (n) => n === undefined || n === null;
        const is_obj = (n) => Object.prototype.toString.call(n) === '[object Object]';
        for (let config of modinfo[configuration]) {
            if (Object.prototype.toString.call(config) !== '[object Object]') {
                continue;
            }
            // 'configuration_options',  # lua_table > list 首先注意，lua中值为nil等于该项不存在，""代表该项为字符串，内容为空
            // # name：该项名称，缺省时该设置项将被忽略，label缺省时显示；label：功能名称位置显示的文字；hover：鼠标悬停按钮时最上方显示的文字
            // # options缺省时该设置项将被忽略，只有一项时其中的data项不可为nil，否则设置时会崩溃。options中只有一项，且该项中desc项为 假 时视为标题，字号加大，hover将被忽略
            // # {{name = "", label = "", hover = "", options = {{ data = "", description = "", hover = ""},}, default = ""}, }

            const {name, hover, label, options, ...others} = config;
            const default_data = others.default;
            if (is_nothing(name) || is_nothing(default_data)) {
                // 视为无效，不显示
                continue;
            }

            // {dataset: [{description: '', data: ?, hover: ''}, ], default_index: '', hover: '', type: '', label: '', name: ''}
            const mod_config = {};

            mod_config.name = name;
            mod_config.hover = hover ?? '';
            mod_config.label = label ?? name;

            if (!Array.isArray(options)) {
                // 不显示，但是添加到配置列表中
                mod_config.type = 'hide';
                mod_config.dataset = [{description: '', data: default_data, hover: ''}];
                mod_config.default_index = 0;
            } else {
                // 清理可能存在的会导致错误的项，并补全可能缺失的 hover，比如不是对象，或者必需项不存在
                for (let i = options.length - 1; i >= 0; i--) {
                    if (is_obj(options[i]) && !is_nothing(options[i].description) && !is_nothing(options[i].data)) {
                        options[i].hover ??= '';
                    } else {
                        delete options[i];
                    }
                }

                if(options.length === 0 || (options.length === 1 && (!options[0].description || (!name && !options[0].data)))) {
                    // 视为标题
                    mod_config.type = 'title';
                    mod_config.dataset = [{description: '', data: default_data, hover: ''}];
                    mod_config.default_index = 0;
                } else {
                    // 视为配置项
                    mod_config.type = 'normal';
                    mod_config.dataset = options;
                    let default_index = 0;
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].data === default_data) {
                            default_index = i;
                            break;
                        }
                    }
                    mod_config.default_index = default_index;
                }
            }
            mod_configs_list.push(mod_config);
        }
    }
    
    modinfo_dataset[modid] ??= Object.fromEntries(mod_configs_list.map(n=>[n.name, n]));

    const empty = !mod_configs_list.filter(n=>n.type !== 'hide').length;

    const ele_no_config = div_();
    ele_no_config.className = `mod_info_none${empty ? '' : ' hide'}`;
    ele_no_config.innerText = '该 mod 不需要配置';
    ele_mod_info_con.appendChild(ele_no_config);
    
    const ele_mod_text = div_();
    ele_mod_text.className = `mod_info_text${empty ? ' hide' : ''}`;
    ele_mod_info_con.appendChild(ele_mod_text);
    const ele_mod_text_opt = div_();
    ele_mod_text_opt.className = `mod_info_text_opt`;
    ele_mod_text_opt.id = `${sign_id}_opt`;
    ele_mod_text.appendChild(ele_mod_text_opt);
    const ele_mod_text_set = div_();
    ele_mod_text_set.className = `mod_info_text_set`;
    ele_mod_text_set.id = `${sign_id}_set`;
    ele_mod_text.appendChild(ele_mod_text_set);
    
    const ele_mod_form = form_();
    ele_mod_form.className = `mod_info_setting${empty ? ' hide' : ''}`;
    ele_mod_form.id = `form_${sign_id}`;
    ele_mod_form.name = sign_id;
    ele_mod_form.autocomplete = 'off';
    ele_mod_info_con.appendChild(ele_mod_form);
    
    for (let conf of mod_configs_list) {
        const {name, label, type, dataset, default_index} = conf;
        const input_id = `${sign_id}_${name}`;

        const ele_setting_item = div_();
        ele_setting_item.className = `cluster_edit_item mod_edit_item${(type === 'hide') ? ' hide' : ''}`;
        const ele_label_out = label_();
        ele_label_out.className = 'cluster_item_label mod_label';
        ele_label_out.htmlFor = input_id;
        ele_label_out.innerText = label.trim();
        ele_setting_item.appendChild(ele_label_out);
        const ele_input_div = div_();
        ele_input_div.className = `cluster_item_div${(type === 'title') ? ' hide' : ''}`;
        ele_setting_item.appendChild(ele_input_div);
        const ele_label_pre = label_();
        ele_label_pre.className = 'label_change_value mod_label_change_value change_value_pre';
        ele_label_pre.htmlFor = input_id;
        ele_label_pre.id = `${input_id}_pre`;
        ele_input_div.appendChild(ele_label_pre);
        const ele_input = input_();
        ele_input.className = 'cluster_item_div_input input_fixed mod_input no_select';
        ele_input.id = input_id;
        ele_input.name = name;
        ele_input.value = dataset[default_index].description;
        ele_input.type = 'text';
        ele_input.readOnly = true;
        ele_input.showtype = type;
        ele_input.dataset.index = default_index.toString();
        ele_input_div.appendChild(ele_input);
        const ele_label_next = label_();
        ele_label_next.className = 'label_change_value mod_label_change_value change_value_next';
        ele_label_next.htmlFor = input_id;
        ele_label_next.id = `${input_id}_next`;
        ele_input_div.appendChild(ele_label_next);

        if (type === 'normal') {
            ele_setting_item.onclick = change_mod_text;
            ele_setting_item.onmouseover = change_mod_text;
            if (default_index === 0) {
                ele_label_pre.setAttribute('disabled', '');
            } else {
                ele_label_pre.onclick = function () {
                    change_value_mod('pre', modid, this);
                }
            }
            if (default_index === dataset.length - 1) {
                ele_label_next.setAttribute('disabled', '');
            } else {
                ele_label_next.onclick = function () {
                    change_value_mod('next', modid, this);
                }
            }
        }

        ele_mod_form.appendChild(ele_setting_item);
    }
    
    if (!document.getElementById(`button_${sign_id}`)) {
        hide_ele(ele_mod_list_placeholder);
        ele_mod_list.appendChild(ele_mod_button);
        ele_info_part.appendChild(ele_mod_info_con);
    }
    run_tried(`add_mod_to_world_${modid}`);
    ele_mod_button.click();
}

function change_mod_text() {
    const ele_input = this.getElementsByTagName('input')[0];
    const index = +ele_input.dataset.index;
    const [mod_sign, modid] = /mod_[^_]+_(\d+)_/.exec(ele_input.id);

    const name = ele_input.name;
    const ele_text_opt = document.getElementById(mod_sign + 'opt');
    const ele_text_set = document.getElementById(mod_sign + 'set');
    
    const text_opt = modinfo_dataset[modid][name].hover ?? '';
    const text_set = modinfo_dataset[modid][name].dataset[index].hover ?? '';

    ele_text_opt.innerText = text_opt;
    ele_text_set.innerText = text_set;
}


function change_value_mod(purpose, verify, label) {
    const input = document.getElementById(label.htmlFor);
    const name = input.name;
    const modinfo = modinfo_dataset?.[verify]?.[name];
    if (!modinfo) {
        return;
    }
    let old_index = +input.dataset.index;
    const {dataset, default_index} = modinfo;

    if (!(0 <= old_index && old_index <= dataset.length - 1)) {
        // 应该什么都不需要做吧
        console.log('channge_value_mod: index超出正常范围，将从 0 开始计算', input);
        old_index = 0;
    }

    // 获取新的 index
    let new_index;
    if (purpose === 'pre') {
        new_index = (old_index === 0) ? old_index : old_index - 1;
    } else if (purpose === 'next') {
        new_index = (old_index === dataset.length - 1) ? old_index : old_index + 1;
    } else {
        console.log('change_value_mod: purpose is wrong !');
        return;
    }

    // 修正 label 的状态
    const label_pre = document.getElementById(input.id + '_pre');
    const label_next = document.getElementById(input.id + '_next');
    if (old_index === 0) {
        label_pre.removeAttribute('disabled');
        label_pre.onclick = function () {
                change_value_mod('pre', verify, this);
            };
    }
    if (old_index === dataset.length - 1) {
        label_next.removeAttribute('disabled');
        label_next.onclick = function () {
                change_value_mod('next', verify, this);
            };
    }
    if (new_index === 0) {
        label_pre.setAttribute('disabled', '');
        label_pre.onclick = null;
    }
    if (new_index === dataset.length - 1) {
        label_next.setAttribute('disabled', '');
        label_next.onclick = null;
    }

    // 赋新值
    input.dataset.index = new_index;
    input.value = dataset[new_index].description;
    input.style.backgroundColor = new_index === default_index ? 'transparent' : 'rgba(127, 127, 127, 20%)';
}


function add_url_param(url, key, value) {
    return url + (url.includes('?') ? '&' : '?') + encodeURIComponent(key) + '=' + encodeURIComponent(value);
}


function tip(text) {
//    TODO 给猪人添加提示
}

function encry() {
    const a = ~~(Math.random() * 10);
    const b = ~~(Math.random() * 10);
    const c = [...[...Array(10)].keys()].join('');
    const d = c.slice(a) + c.slice(0, a);
    const e = Date.now().toString().slice(0, 10);
    const f = e.slice(b) + e.slice(0, b);
    return '' + a + b + (+d + +f);
}
encry()
