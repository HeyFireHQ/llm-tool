mod llm_tool::llm_tool;

#[test]
fn should_be_ok() {
    llm_tool::get_param_descriptions();
    assert_eq!(1, 2);
}
