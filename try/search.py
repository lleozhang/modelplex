<!DOCTYPE html>
<html lang="zh-cn">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<title>搜索</title>
		<link type="text/css" rel="stylesheet" href="/static/css/bootstrap.min.css" />
		<link type="text/css" rel="stylesheet" href="/static/css/bootstrap-theme.min.css" />
		<link type="text/css" rel="stylesheet" href="/static/css/uoj-theme.css" />
	</head>
    <body role="document">
		<div class="container theme-showcase" role="main">
			{% include "headerbar.html" %}

                <div class="uoj-content">
                    <h2 class="page-header">搜索</h2><br><br>
                    <form action="/modelplex/search_result" id="search_result" class="form-horizontal" method="get">
                        <div id="div-username" class="form-group">
                            <label for="input-username" class="col-sm-2 control-label"></label>
                            <div class="col-sm-3">
                              <input type="text" oninput="value=value.replace(/[^\w\u4E00-\u9FA5]/g, '')"  class="form-control" id="input-username" name="q" placeholder="在此键入模型关键词..." maxlength="20" />
                              <!--<span class="help-block" id="help-username"></span>-->
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="col-sm-offset-2 col-sm-3">
                              <button type="submit" id="button-submit" class="btn btn-default">搜索相关模型！</button>
                            </div>
                        </div>
                    </form>                    
		<form action="/modelplex/search_dataset_result" id="search_dataset_result" class="form-horizontal" method="get">
			<div id="div-username" class="form-group">
                            		<label for="input-username" class="col-sm-2 control-label"></label>
                            			<div class="col-sm-3">
                              			<input type="text" oninput="value=value.replace(/[^\w\u4E00-\u9FA5]/g, '')"  class="form-control" id="input-username" name="q" placeholder="在此键入数据集关键词..." maxlength="20" />
                              		<!--<span class="help-block" id="help-username"></span>-->
                            			</div>
                        	</div>    
                        <div class="form-group">
                            <div class="col-sm-offset-2 col-sm-3">
                              <button type="submit" id="button-submit" class="btn btn-default">搜索相关数据集！</button>
                            </div>
                        </div>
                    </form>

                  </div>
                </div>
    </body>
</html>
