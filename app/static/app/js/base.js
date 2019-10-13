function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function change_ignore_event (){
    let csrftoken = getCookie('csrftoken');
    let site_pk = this.value;
    let checked = this.getAttribute('checked');
    $.ajax({
        url: 'change_ignore/',
        type: 'POST',
        data: {'csrfmiddlewaretoken': csrftoken, 'site_pk': site_pk, 'checked': checked},
        success: function (data){

        },
        error: function (xhr){
            console.log(xhr);
        }
    });
}


// 检测字符串是否为空
function isEmpty(obj){
    if(typeof obj == "undefined" || obj == null || obj.trim() == ""){
        return true;
    }else{
        return false;
    }
}


window.onload = function (){
    // 显示编辑站点的表单。
    function editorBtn(){
        let name = this.getAttribute("data-name");
        let href = this.getAttribute("data-href");
        let coding = this.getAttribute("data-coding");
        let need_verification = this.getAttribute("data-verification");
        let overseas = this.getAttribute("data-overseas");
        let restart_file = this.getAttribute("data-restart");
        let deploy_file = this.getAttribute("data-deploy");
        let update_cert = this.getAttribute("data-update-cert");
        let copy = this.getAttribute("data-copy");


        name_input.value = name;
        href_input.value = href;
        coding_input.value = (coding === 'None')? '':coding;
        restart_input.value = (restart_file === 'None')? '':restart_file;
        deploy_input.value = (deploy_file === 'None')? '':deploy_file;
        update_cert_input.value = (update_cert === 'None')? '':update_cert;
        copy_input.value = (copy === 'None')? '':copy;

        if (need_verification === 'False'){
            verification_input.checked = false;
        }else{
            verification_input.checked = true;
        }


        if (overseas === 'False'){
            overseas_input.checked = false;
        }else{
            overseas_input.checked = true;
        }

        add_site_btn.setAttribute('site-id', this.getAttribute('data-num'));
        showElement(popo);
        showElement(popo_content);
    }
   
    // 给新增加的checkbox增加点击事件
    function need_select_all_checkbox(){
        let count = 0;
        let item;
        for (item of is_verification_checkboxs){
            if (item.checked == true){
                count += 1;
            }
        };
        if (count == is_verification_checkboxs.length){
            select_all_checkbox.checked = true;
        }else{
            select_all_checkbox.checked = false;
        }
    }

    function hideElement(obj, no_reset){
        // 每次隐藏重置form
        obj.style.display = 'none';
        let reset = no_reset || true;
        if (reset){
            form.reset();
        }
    }

     function showElement(obj){
        obj.style.display = 'block';
    }


    function delete_site(){
        let is_delete = confirm("此操作会删除记录,是否继续");

        if (is_delete){
            let site_id = this.getAttribute('data-num');
            let csrf_token = getCookie('csrftoken');
            let self = this;
            $.ajax({
                url: 'delete_site/',
                type: 'post',
                data: {"site_id": site_id, "csrfmiddlewaretoken": csrf_token},
                success: function (data){
                    let code = data.code;
                    if (code === 200){
                        self.parentElement.parentElement.remove();
                        let html = $(data.data.html);
                        $('body').prepend(html);
                        setTimeout(function (){
                            html.fadeOut(1000, function (){
                                this.remove();
                            });
                        }, 1500);
                    }
                },
                error: function (xhr){
                    console.log(xhr);
                }
            })
        }
    }

    let popo_close = document.querySelector(".popo-close");  // 关闭popo框按钮
    let popo = document.querySelector('.popo');
    let popo_content = document.querySelector('.popo .popo-content');
    let add_site_btn = document.querySelector('#add-site-btn');

    let concel_add_site = document.querySelector('#concel-add-site');
    // 增加编辑站点表单
    let form = document.querySelector('#add-site-form');
    let start_verification = document.querySelector('#start-verification');

    let add_site = document.querySelector("#add-site");

    let editor_site_btns = document.querySelectorAll("a[data-type='editor-site']");
    let delete_site_btns = document.querySelectorAll("a[data-type='delete-site']");

    let site_tbody = $('tbody')[0];

    let show_site_description_trs = document.querySelectorAll('tr[name="show-site-description"]');
    let site_description_trs = document.querySelectorAll("tr[name='site-description']");

    let is_ignore_checkboxs = document.getElementsByName('is-ignore');
    let select_all_checkbox = document.getElementById('select-all');
    var is_verification_checkboxs = document.querySelectorAll('input[name="site-pk-checkbox"]');


    // form表单input
    let name_input = form.querySelector("input[name='name']");
    let href_input = form.querySelector("input[name='href']");
    let coding_input = form.querySelector("input[name='coding']");
    let verification_input = form.querySelector("input[name='custom-switch-checkbox']");
    let overseas_input = form.querySelector("input[name='overseas-switch-checkbox']");
    let restart_input = form.querySelector("input[name='restart']");
    let deploy_input = form.querySelector("input[name='deploy']");
    let update_cert_input = form.querySelector("input[name='update_cert']");
    let copy_input = form.querySelector("input[name='copy']");


    if (select_all_checkbox){
        select_all_checkbox.onclick = function (){
            if (this.checked == true){
                is_verification_checkboxs.forEach(function (elem){
                    elem.checked = true;
                });
            }else{
                is_verification_checkboxs.forEach(function (elem){
                    elem.checked = false;
                });
            }
            
        };
    }
    

    is_verification_checkboxs.forEach(function (elem){
        elem.onclick = need_select_all_checkbox;
    });


    is_ignore_checkboxs.forEach(function (elem){
        elem.onchange = change_ignore_event;
    });


    // 给站点检测历史记录增加点击事件。 显示站点检测历史记录的隐藏信息
    show_site_description_trs.forEach(function (elem){
        elem.addEventListener('click', function (){
            $(this.nextElementSibling).toggle();
            $(this.nextElementSibling).siblings("tr[name='site-description']").hide();
        });
    });

    add_site.onclick = function (){
        showElement(popo);
        showElement(popo_content);
        add_site_btn.removeAttribute('site-id');
    };

    popo_close.onclick = function (){
        hideElement(popo);
    };

    // who：添加站点的form中的取消按钮，作用：隐藏增加站点编辑框
    concel_add_site.addEventListener('click', function(e){
        hideElement(popo);
        e.preventDefault();
    });

    // 编辑站点信息
    editor_site_btns.forEach(function (elem){
        elem.addEventListener('click', editorBtn);
    });

    // who: 删除站点按钮 作用：给每个删除按钮增加点击事件
    delete_site_btns.forEach(function (elem){
        elem.addEventListener('click', delete_site);
    });

    // who: popo框的确定按钮， 作用： 增加修改站点
    add_site_btn.addEventListener('click', function (e){

        let site_id = this.getAttribute("site-id") || '';

        let form = $('#add-site-form');
        let self = this;
        $.ajax({
            url: 'add_site/',
            type: 'post',
            data: form.serialize()+'&site_id='+site_id,
            success: function (data){
                if (data.code === 200)
                {
                    let site_tr_html = $(data.data.site_tr_html);
                    let editor_site_btn = $(site_tr_html).find("a[data-type='editor-site']")[0];
                    let delete_site_btn = $(site_tr_html).find("a[data-type='delete-site']")[0];
                    let site_pk_checkbox = $(site_tr_html).find("input[name='site-pk-checkbox']")[0];
                    let ignore_checkbox = $(site_tr_html).find("input[name='is-ignore']")[0];
                    
                    site_pk_checkbox.addEventListener('click', need_select_all_checkbox);
                    ignore_checkbox.addEventListener('click', change_ignore_event);
                    editor_site_btn.addEventListener('click', editorBtn);
                    delete_site_btn.addEventListener('click', delete_site);
                    let msg_html = $(data.data.msg_html);
                    $('body').prepend(msg_html);
                    // 弹出消息框
                    setTimeout(function (){
                        msg_html.fadeOut(1000, function (){
                            this.remove();
                        });
                    }, 1500);
                    hideElement(popo);

                    // 在table中添加tr记录
                    if (data.data.action == 'create'){
                        $(site_tbody).append(site_tr_html);
                    }else{
                        let site_id = data.data.site_id;
                        let $tr = $(`tr[data-num="${site_id}"]`);
                        $tr.replaceWith(site_tr_html);
                    }
                    is_verification_checkboxs = document.querySelectorAll('input[name="site-pk-checkbox"]');
                }else{
                    let msg_html = $(data.data.msg_html);
                    $('body').prepend(msg_html);
                    setTimeout(function (){
                        msg_html.fadeOut(1000, function (){
                            this.remove();
                        });
                    }, 1500);
                }
                
            },
            error: function (xhr){
                console.log(xhr);
            }

        })
    });

    // 点击检测站点按钮
    start_verification.addEventListener('click', function (){
        // document.querySelectorAll('input[name=""]')
        let verification_site_form = document.getElementById('verification_site_form');
        verification_site_form.submit();
    });


    var mask = document.querySelector("div.mask");

    // 执行脚本文件
    function run_script(event){
        let action = this.getAttribute("data-action");
        let id = this.getAttribute("data-id");
        let csrftoken = getCookie("csrftoken");

        showElement(mask);

        $.ajax({
            url: '/run_script/',
            type: 'post',
            data: {'site_id': id, "action": action, 'csrfmiddlewaretoken': csrftoken},
            success: function (data){
                hideElement(mask);

                alert(data.msg);
            },  
            error: function (xhr){
                console.log(xhr);
                hideElement(mask);
                alert("服务器内部错误");
            }
        });

        event.preventDefault();
    }


    // 执行脚本按钮
    $('body').delegate("td[name=run-script] button", 'click', run_script);

};
