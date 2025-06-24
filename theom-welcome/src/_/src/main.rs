use web_view::*;

fn main() {
    let html = include_str!("keybindings.html");

    web_view::builder()
        .title("Keyboard Shortcuts")
        .content(Content::Html(html))
        .size(600, 400)
        .resizable(true)
        .debug(false)
        .user_data(())
        .invoke_handler(|_webview, _arg| Ok(()))
        .run()
        .unwrap();
}
